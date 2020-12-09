<template>
    <div class="chat-message-input-container">
        <div class="input_msg_write">
            <input
                type="text"
                class="write_msg"
                placeholder="Type a message..."
                v-model="input_message"
                v-on:keyup.enter="send"
            />
            <v-btn class="msg_send_btn" @click="send">
                <v-icon style="color: #05728f">fa fa-paper-plane</v-icon>
            </v-btn>
        </div>
    </div>
</template>

<script>
import { mapState, mapMutations, mapActions } from "vuex";

export default {
    data() {
        return {
            input_message: "",
        };
    },

    computed: {
        conversation() {
            return this.$store.state.conversation;
        },
        active_user() {
            return this.$store.state.active_chat_user;
        },
    },

    methods: {
        send() {
            let now = new Date();
            let message_datetime = now.toLocaleString();
            this.$fire.firestore.collection("message").add({
                sender: this.$auth.user.username,
                receiver: this.active_user.username,
                message: this.input_message,
                createdAt: now,
                message_datetime: message_datetime,
            });

            this.input_message = "";
        },
        ...mapActions({
            update: "updateConversation",
        }),
        ...mapMutations({
            sendMessage: "sendMessage",
        }),
    },
};
</script>
