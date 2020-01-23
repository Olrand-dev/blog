const Utils = {

    data() {
        return {

        }
    },

    methods: {

        objLength(obj) {
            return Object.keys(obj).length;
        }
    }
};


const CsrfToken = {

    data() {
        return {
            csrfToken: '',
        }
    },

    created() {
        this.csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
    },
};