<template>
    <div v-bind:class="message.sender === $auth.user.username ? 'outgoing_msg' : 'incoming_msg'">
        <div class="incoming_msg_img">
            <img
                :src="getImage(active_chat_user_image)"
                v-if="message.sender !== $auth.user.username"
            />
        </div>
        <div v-bind:class="message.sender === $auth.user.username ? 'sent_msg' : 'received_msg'">
            <div v-bind:class="message.sender === $auth.user.username ? '' : 'received_withd_msg'">
                <p>{{ message.message }}</p>
                <span class="time_date"> {{ message.message_datetime }}</span>
            </div>
        </div>
    </div>
</template>

<script>
import { mapState, mapMutations, mapActions } from "vuex";

export default {
    name: "Message",
    props: ["message"],

    data() {
        return {
            interval: null,
        };
    },

    // Getting the values from Store
    computed: {
        active_chat_user_image() {
            return this.$store.state.active_chat_user_image;
        },
        active_chat_user() {
            return this.$store.state.active_chat_user;
        },
    },

    methods: {
        getImage(image) {
            return require("../assets/profile/" + image);
        },
    },
};
</script>

<style></style>
