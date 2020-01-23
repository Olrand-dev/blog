const RESP_STATUS_SUCCESS = 'success';
const RESP_STATUS_ERROR = 'error';
const RESP_STATUS_SERVER_ERROR = 'server_error';
const RESP_ALIAS_REDIRECT = 'redirect';

$(document).ready(function() {

    $(document).ajaxSuccess(function(event, request, options, data) {
        
        if (data.status === RESP_STATUS_ERROR) {
            errorToast(data.message);
        }
        if (data.status === RESP_STATUS_SERVER_ERROR) {
            serverErrorToast(data.message);
        }
        if (data.status === RESP_STATUS_SUCCESS && data.alias === RESP_ALIAS_REDIRECT) {
            window.location.href = data.data;
        }
    });


    $.ajax({
        url: '/get-user-data',
        type: 'GET',
        dataType: 'json',
        data: {},
        success: function(response) {
            
            let data = response.data;

            store.commit('setUserAuth', data.user_auth);
            store.commit('setUserId', data.user_id);
            store.commit('setUserGroup', data.user_group);
            store.commit('setUserLogin', data.user_login);
            store.commit('setUserName', data.user_name);

        }.bind(this)
    });
});

Vue.use(Vuex);

const store = new Vuex.Store({

    state: {

        userAuth: false,
        userId: 0,
        userGroup: '',
        userLogin: '',
        userName: '',
    },

    mutations: {

        setUserAuth(state, bool) {
            state.userAuth = bool;
        },

        setUserId(state, val) {
            state.userId = val;
        },

        setUserGroup(state, val) {
            state.userGroup = val;
        },
        setUserLogin(state, val) {
            state.userLogin = val;
        },
        setUserName(state, val) {
            state.userName = val;
        },
    },

    getters: {

    }
});


function hop(obj, prop) {
    if (!isObject(obj)) return false;
    return obj.hasOwnProperty(prop);
}

function isObject(val, orFunction = false) {
    if (val === null) return false;
    return (orFunction) ? ((typeof val === 'function') || (typeof val === 'object')) : typeof val === 'object';
}

function objLength(obj) {
    return Object.keys(obj).length;
}

function clone(obj, deep = false) {
    if (!isObject(obj)) return;

    return (deep) ? jQuery.extend(true, {}, obj) : jQuery.extend({}, obj);
}

function getRandomInt(max) {
    return Math.floor(Math.random() * Math.floor(max));
}

function smartTrim(string, maxLength) {
    let trimmedString = string.substr(0, maxLength);
    return trimmedString.substr(0, Math.min(trimmedString.length, trimmedString.lastIndexOf(" ")));
}