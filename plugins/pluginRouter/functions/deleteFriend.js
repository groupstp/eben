import {sender} from "./baseClasses/sendClass";
import {addFriend} from "./addFriend"

class pluginClass extends addFriend{
    constructor(){
        super(name);
    }

    /**
     * Разрыв связей между пользователями(удаление из друзей)
     * @param project
     * @param user
     * @param friend
     * @returns {*}
     * @private
     */
    __deleteFriend(project, user, friend){
        return sender.send({
            object: `${project}.friends`,
            method: "delete",
            parameters: {
                filter: this.__getFilterForFriend(user, "friendID", friend)
            }
        });
    }

    async run(parameters, token, deep = 0){
        this.__checkParameters(parameters);

        let {project, object} = parameters.parameters;
        let friend = parameters.values[0].friend;

        if (await this.__checkFriend(project, "friends", "friend", object, friend)) {
            await this.__deleteFriend(project, object, friend);
            await this.__deleteFriend(project, friend, object);
            await this.__addRequest(project, object, friend);
            await this.__addSentRequest(project, friend, object);
        }
        else if (!await this.__checkFriend(project, "friendsRequests", "sent_request", object, friend)){
            await this.__deleteRequest(project, object, "sent_request", friend);
        }
        else {
            throw "Невозможно удалить пользователя, которого нет ни в друзьях ни в заявках на добавление в друзья."
        }
    }
}

let name = "deleteFriend";
let plugin = new pluginClass();

export {
    plugin as plugin,
    name as name
}
