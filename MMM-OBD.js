Module.register("MMM-OBD", {
	// Default module config.
	defaults: {},
	text: 'Scanning for OBD...',

	// Return the scripts that are necessary for the weather module.
	getScripts: function () { return []; },

	start: function() {
		Log.log(this.name + ' is started!');
		this.sendSocketNotification('MIRROR_START', this.config);		
	},

	socketNotificationReceived: function (notification, payload) {
		console.log(payload.msg);
		if (notification === "PYTHON") {
			this.text = payload.msg;
			this.updateDom();
		}
		else if(notification === "loop"){ Log.log("Loop"); }
		else{ 
			Log.log("No python");
			this.sendSocketNotification('MIRROR_START', this.config);
		}
	},
	// Override dom generator.
	getDom: function() {
		var wrapper = document.createElement("div");
		wrapper.innerHTML = this.text;
		return wrapper;
	}
});
