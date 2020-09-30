var ESB = require('light-esb-node');

module.exports = class EsbImplementation{
    constructor(sender, senderSystem, id){
        this.sender = sender;
        this.senderSystem = senderSystem;
        this.id = id;
    }

    sendMessage(payload, channel){
        var message = ESB.createMessage(payload, channel, this.senderSystem, this.id)
        this.component.send(message);
    }

    configureEsb(){
        this.component = ESB.createLoggerComponent(this.esbCallback);
        this.receiver1 = ESB.createRouteComponent(this.esbCallback, {
            routeItems: [
                {
                    routeFunction: function(esbMessage){
                        var comparison = esbMessage.context.caller.user;
                        if(comparison == "Male")
                            return true;
                        return false;
                    },
                    channel: "Male"
                },
                {
                    routeFunction: function(esbMessage){
                        var comparison = esbMessage.context.caller.user;
                        if(comparison == "female" || comparison == "Female")
                            return true;
                        return false;
                    },
                    channel: "Female"
                },
                {
                    routeFunction: function(esbMessage){
                        if(esbMessage.context.caller.user!="male" && esbMessage.context.caller.user!="female" && esbMessage.context.caller.user!="Male" && esbMessage.context.caller.user!="Female" )
                            return true;
                        return false;
                    },
                    channel: "Other"
                }
            ]
        });

        this.male_component = ESB.createScriptComponent(this.esbCallback, function(esbMessage, callback){
            console.log("Male");
            console.log("Message is", esbMessage);
        });

        this.female_component = ESB.createScriptComponent(this.esbCallback, function(esbMessage, callback){
            console.log("Female");
            console.log("Message is", esbMessage);
        });

        this.other_component = ESB.createScriptComponent(this.esbCallback, function(esbMessage, callback){
            console.log("Other");
            console.log("Message is", esbMessage);
        });

        this.component.connect(this.receiver1);
        this.receiver1.connect("Male", this.male_component);
        this.receiver1.connect("Female", this.female_component);
        this.receiver1.connect("Other", this.other_component);
    }

     esbCallback(error, message){
        if(error){
            console.log('Error while processing the message\n', error, message);
        }
        else{
            console.log('Message received...');
            console.log('Message: ', message);
            console.log('Processing')
        }
    }


};