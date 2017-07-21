AFRAME.registerComponent('log', {
	
	schema: {
		event: {type: 'string', default: ''},
		message: {type: 'string', default: 'Hello, World!'}
	},

	init: function () {
		var self = this;

		this.eventHandlerFn = function () { console.log(self.data.message); };
	},

	update: function() {
		var data = this.data;
		var el = this.el;

		if (data.event) {
			el.addEventListener(data.event, this.eventHandlerFn);
		} else {
			console.log(data.message)
		}
	}
});