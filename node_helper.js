'use strict';
const NodeHelper = require('node_helper');
const Log = require('logger');
const {PythonShell} = require('python-shell');

module.exports = NodeHelper.create({
  // Override start method.
  start: function () {
    Log.log("Starting node helper for: " + this.name);
    var self = this;
    this.io.on('connection', function(socket){
      Log.log('User connected: ' + socket.id);
      
      socket.on('disconnect', function () {
        Log.log('User disconnected: ' + socket.id);
      });

      socket.on('chat message', (message) => {
        Log.log('message: ' + message);
        if(message.includes("loop")){ self.sendSocketNotification("loop", {msg:message}); }
        else{ self.sendSocketNotification("PYTHON", {msg:message}); }
      });
    });
    
  },

  python_start: function () {
    let pyshell = new PythonShell('modules/' + this.name + '/obd_monitor.py');    //pyshell.send('hello');
    var self = this; 
    
    pyshell.on('message', function ( message ) {
    });

    // end the input stream and allow the process to exit
    pyshell.end(function ( err, code, signal ) {
      if (err) throw err;
      console.log('Python finished');
      self.sendSocketNotification('MIRROR_START', "");
    });
  },

  socketNotificationReceived: function( notification, payload ) {
    if(notification === 'MIRROR_START') {
      var self = this
      var current = new Date();
      
      if( current.getHours()>7 ){
        self.python_start();
      }
      else{
        Log.log("Outside run time");
        setTimeout(function(){
          self.sendSocketNotification('MIRROR_START', "");
        }, 60*1000);
      }
    };
  }

});
