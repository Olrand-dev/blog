const RESP_STATUS_SUCCESS = 'success';
const RESP_STATUS_ERROR = 'error';
const RESP_STATUS_SERVER_ERROR = 'server_error';
const RESP_ALIAS_REDIRECT = 'redirect';

$(document).ready(function () {

    $(document).ajaxSuccess(function (event, request, options, data) {

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


    $('a.header__search-trigger').click(function () {
        $(this).modal({
            fadeDuration: 200
        });
        return false;
    });


    /* $.ajax({
        url: '/get-user-data',
        type: 'GET',
        dataType: 'json',
        data: {},
        success: function (response) {

            

        }.bind(this)
    }); */
});


Vue.use(VueToast);

function successToast(msg, duration = 3200) {
    Vue.$toast.open({
        message: msg,
        type: 'success',
        position: 'top-right',
        duration: duration
    });
}

function infoToast(msg, duration = 3200) {
    Vue.$toast.open({
        message: msg,
        type: 'info',
        position: 'top-right',
        duration: duration
    });
}

function warningToast(msg, duration = 4200) {
    Vue.$toast.open({
        message: msg,
        type: 'warning',
        position: 'top-right',
        duration: duration
    });
}

function errorToast(msg, duration = 5000) {
    Vue.$toast.open({
        message: msg,
        type: 'error',
        position: 'top-right',
        duration: duration
    });
}

function serverErrorToast(msg, duration = 15000) {
    Vue.$toast.open({
        message: msg,
        type: 'error',
        position: 'top-right',
        dismissible: false,
        duration: duration
    });
}


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