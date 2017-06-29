// Copyright (c) 2017 Jakub Boksansky, Adam Pospisil - All Rights Reserved
// Wilberforce Wireframe Unity Shader 0.9beta

using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEditor;
using System;

namespace Wilberforce.Wireframe
{
    public class WilberforceWireframeShaderGUI : ShaderGUI
    {
        public override void OnGUI(MaterialEditor materialEditor, MaterialProperty[] properties)
        {
            Material targetMat = materialEditor.target as Material;

            float wireThickness = targetMat.GetFloat("_WireThickness");
            float capSize = targetMat.GetFloat("_CapSize");

            targetMat.SetFloat("_WireThickness", Mathf.Max(0.0f, wireThickness));
            targetMat.SetFloat("_CapSize", Mathf.Max(0.0f, capSize));

            base.OnGUI(materialEditor, properties);

        }
    }
}