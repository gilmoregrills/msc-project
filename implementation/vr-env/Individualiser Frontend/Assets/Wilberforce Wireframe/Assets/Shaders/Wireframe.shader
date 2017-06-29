// Upgrade NOTE: replaced 'mul(UNITY_MATRIX_MVP,*)' with 'UnityObjectToClipPos(*)'

// Copyright (c) 2017 Jakub Boksansky, Adam Pospisil - All Rights Reserved
// Wilberforce Wireframe Unity Shader 0.9beta

Shader "Wilberforce/Wireframe"
{
	Properties
	{
		_WireThickness ("Wire Thickness", Float) = 1
		_WireColor ("Wire Color", Color) =  (0, 0, 0, 1)
		_FillColor ("Fill Color", Color) =  (1, 1, 1, 1)
		[MaterialToggle] _RemoveDiagonal ("Remove Diagonals", Int) = 0
		[MaterialToggle] _FlatShading ("Apply Flat Shading", Int) = 0
		[MaterialToggle] _ObjectSpace ("Calculate in Object Space (Perspective)", Int) = 1
		[MaterialToggle] _Caps ("Show Line Caps (Beta)", Int) = 0
		_CapSize ("Line Caps Size", Float) = 1
		[Enum(Back,1,Front,2)] _CullingSetting ("Apply to faces", Int) = 2
	}
	SubShader
	{

		Tags { "RenderType" = "Transparent" "Queue" = "Transparent" }
		Blend SrcAlpha OneMinusSrcAlpha
		Cull [_CullingSetting]
		ZWrite On

		Pass
		{
			CGPROGRAM

			#pragma vertex vert
			#pragma fragment frag
			#pragma geometry geom

			#include "UnityCG.cginc"

			uniform float _WireThickness;
			uniform float4 _WireColor;
			uniform float4 _FillColor;
			uniform int _RemoveDiagonal;
			uniform int _ObjectSpace;
			uniform int _FlatShading;
			uniform int _Caps;
			uniform float _CapSize;
			
			struct appdata
			{
				float4 vertex : POSITION;
				float3 normal : NORMAL;
				float2 uv : TEXCOORD0;
			};

			struct v2f
			{
				float4 vertex : SV_POSITION;
				float2 normal : NORMAL;
				float4 vertexObject : TEXCOORD3;
				float shade : TEXCOORD4;
				float4 bar : TEXCOORD5;
				float4 dist : TEXCOORD1;
				float4 edgeLength : TEXCOORD2;
			};

			v2f vert (appdata v)
			{
				v2f o;
				#if UNITY_VERSION >= 540
				o.vertex = UnityObjectToClipPos(v.vertex);
				#else
				o.vertex = UnityObjectToClipPos(v.vertex);
				#endif
				o.vertexObject = mul (UNITY_MATRIX_MV, v.vertex);
				o.edgeLength = float4(0, 0, 0, 0);
				o.dist = float4(0, 0, 0, 1);
				o.bar = float4(0, 0, 0, 1);
				o.normal = float2(0, 0);
				o.shade = 1.0f;
				return o;
			}

			[maxvertexcount(3)]
            void geom(triangle v2f input[3], inout TriangleStream<v2f> OutputStream)
            {
				float aspect = _ScreenParams.x / _ScreenParams.y;
			    float2 p0 = float2(input[0].vertex.x * aspect, input[0].vertex.y) / input[0].vertex.w;
				float2 p1 = float2(input[1].vertex.x * aspect, input[1].vertex.y) / input[1].vertex.w;
				float2 p2 = float2(input[2].vertex.x * aspect, input[2].vertex.y) / input[2].vertex.w;

				float2 v0 = p2-p1;
				float2 v1 = p2-p0;
				float2 v2 = p1-p0;
				
				float area = abs(v1.x*v2.y - v1.y * v2.x);

                v2f output = (v2f) 0;

				float lengthV0 = length(v0);
				float lengthV1 = length(v1);
				float lengthV2 = length(v2);
				
				float3 v0Object = input[2].vertexObject.xyz - input[1].vertexObject.xyz;
				float3 v1Object = input[2].vertexObject.xyz - input[0].vertexObject.xyz;
				float3 v2Object = input[1].vertexObject.xyz - input[0].vertexObject.xyz;

				float areaObject = length(cross(v1Object, v2Object)) * 0.5f;

				float3 normal = normalize(cross(v2Object, v1Object));
				float shade = abs(dot(normal, normalize(input[0].vertexObject.xyz)));

				float lengthV0Object = length(v0Object);
				float lengthV1Object = length(v1Object);
				float lengthV2Object = length(v2Object);

				float4 lengthObject = float4(lengthV0Object,
											 lengthV1Object,
											 lengthV2Object,
											 area);

                output.vertex = input[0].vertex;
				output.edgeLength = lengthObject;
				output.shade = shade;
				if (_ObjectSpace != 0) {
					output.dist = float4(areaObject / lengthV0Object, 0, 0, 1);
				} else {
					output.dist = float4(area / lengthV0, 0, 0, 1);
				}
				output.bar = float4(1, 0, 0, 1);
                OutputStream.Append(output);

				output.vertex = input[1].vertex;
				output.edgeLength = lengthObject;
				output.shade = shade;
				if (_ObjectSpace != 0) {
					output.dist = float4(0, areaObject / lengthV1Object, 0, 1);
				} else {
					output.dist = float4(0, area / lengthV1, 0, 1);
				}
				output.bar = float4(0, 1, 0, 1);
                OutputStream.Append(output);

				output.vertex = input[2].vertex;
				output.edgeLength = lengthObject;
				output.shade = shade;
				if (_ObjectSpace != 0) {
					output.dist = float4(0, 0, areaObject / lengthV2Object, 1);
				} else {
					output.dist = float4(0, 0, area / lengthV2, 1);
				}
				output.bar = float4(0, 0, 1, 1);
                OutputStream.Append(output);
            }

			float wireframe(v2f i) {
				float d;
				float e;
				if (_RemoveDiagonal != 0) {
					if (i.edgeLength.x > i.edgeLength.y && i.edgeLength.x > i.edgeLength.z) {
						d = min(i.dist[1], i.dist[2]);
					} else if (i.edgeLength.y > i.edgeLength.x && i.edgeLength.y > i.edgeLength.z) {
						d = min(i.dist[0], i.dist[2]);
					} else {
						d = min(i.dist[1], i.dist[0]);
					}
				} else {
					d = min(i.dist[0], min(i.dist[1], i.dist[2]));
				}
				
				e = max(i.bar[0], max(i.bar[1], i.bar[2]));
				_CapSize = _CapSize * 0.1f;
				if (_Caps != 0) d = d*(1-(_CapSize *e));
				return smoothstep(0.0f, (abs(_WireThickness) * 0.001f), d);
			}

			
			fixed4 frag (v2f i) : SV_Target
			{
				float shade = 1.0f;
				if (_FlatShading != 0) shade = i.shade;
				return lerp(_WireColor, float4(shade * _FillColor.rgb, _FillColor.a), wireframe(i));
			}

			ENDCG
		}
	}
	CustomEditor "Wilberforce.Wireframe.WilberforceWireframeShaderGUI"
}
