AFRAME.registerComponent('sourceFTL', {
	
	init: function () {
		var self = this;

		var audioContext = new AudioContext();
		var audioElementSource = 
			audioContext.createMediaElementSource(this);
		var foaRenderer = Omnitone.createFOARenderer(audioContext, {
			HRIRUrl = 'https://cdn.rawgit.com/GoogleChrome/omnitone/962089ca/build/resources/sh_hrir_o_1.wav'
		});

		foaRenderer.initializer().then(function() {
			audioElementSource.connect(foaRenderer.input);
			foaRenderer.output.connect(audioContext.destination);
			audioElement.play();
		});
	}

});