<template>
    <div class="chatpage-container">
        <h3 class="text-center" style="margin: 15px 0px">Live Chat</h3>
        <div class="main-container">
            <div class="left-container">
                <div class="header-container">
                    <div class="header">
                        <h4>Recent</h4>
                    </div>
                </div>

                <div class="users-container">
                    <!-- component 1 - user -->
                    <User v-for="user in users" :key="user.id" :user="user" />
                </div>
            </div>

            <div class="right-container">
                <!-- component 2 - MessageBox -->
                <div ref="chatMessageContainer" class="chat-message-container">
                    <Message v-for="message in conversation" :key="message.id" :message="message" />
                </div>

                <!-- component 3 - Message Input -->
                <MessageInput />
            </div>
        </div>
    </div>
</template>

<script>
import User from "../../components/User";
import Message from "../../components/Message";
import MessageInput from "../../components/MessageInput";
import { mapState, mapMutations, mapActions } from "vuex";

export default {
    head: {
        title: "Vueducation - Chat",
    },
    data() {
        return {
            users: [],
            interval: null,
        };
    },

    middleware: ["auth"],

    components: {
        User,
        Message,
        MessageInput,
    },

    mounted() {
        this.get_chat_users();
    },

    computed: {
        conversation() {
            return this.$store.state.conversation;
        },

        active_chat_user() {
            return this.$store.state.active_chat_user;
        },
    },

    methods: {
        ...mapMutations({
            toggle: "toggleSelected",
        }),

        ...mapActions({
            update: "updateConversation",
        }),

        async get_chat_users() {
            try {
                let currentUser = this.$auth.user.username;

                const ref = this.$fire.firestore.collection("conversation").doc(currentUser);
                let snap;
                try {
                    snap = await ref.get();
                    let friends = snap.data().friends;
                    for (let friend of friends) {
                        let response = await this.$axios.get("/api/users/" + friend);
                        this.users.push(response.data);
                    }
                } catch (e) {
                    console.error(e);
                }
                this.toggle(this.users[0]);
                this.update(this.users[0]);
            } catch (error) {
                console.error(e);
            }
        },

        async loop_messages() {
            let currentUser = this.$auth.user.username;
            try {
                this.$fire.firestore
                    .collection("message")
                    .orderBy("createdAt")
                    .onSnapshot((querySnapshot) => {
                        var allMessages = [];
                        querySnapshot.forEach((doc) => {
                            let sender = doc.data().sender;
                            let receiver = doc.data().receiver;

                            if (
                                sender == this.active_chat_user.username &&
                                receiver == currentUser
                            ) {
                                allMessages.push(doc.data());
                            }

                            if (
                                sender == currentUser &&
                                receiver == this.active_chat_user.username
                            ) {
                                allMessages.push(doc.data());
                            }
                        });
                        this.conversation = allMessages;
                    });
            } catch (e) {
                console.error(e);
            }
        },
    },
};
</script>

<style>
.incoming_msg_img {
    display: inline-block;
    width: 6%;
}

.user-image {
    float: left;
    width: 11%;
}

/* Will change v-container */
.chatpage-container {
    max-width: 1170px;
    margin: auto;
}

img {
    max-width: 100%;
}

.left-container {
    background: #f8f8f8 none repeat scroll 0 0;
    float: left;
    overflow: hidden;
    width: 40%;
    border-right: 1px solid #c4c4c4;
}

.main-container {
    border: 1px solid #c4c4c4;
    clear: both;
    overflow: hidden;
}

.top_spac {
    margin: 20px 0 0;
}

.search_bar {
    display: inline-block;
    text-align: right;
    width: 60%;
}

.header-container {
    padding: 10px 29px 10px 20px;
    overflow: hidden;
    border-bottom: 1px solid #c4c4c4;
}

.header h4 {
    color: #05728f;
    font-size: 21px;
    margin: auto;
}

.search_bar input {
    border: 1px solid #cdcdcd;
    border-width: 0 0 1px 0;
    width: 80%;
    padding: 2px 0 4px 6px;
    background: none;
}

.search_bar .input-group-addon button {
    background: rgba(0, 0, 0, 0) none repeat scroll 0 0;
    border: medium none;
    padding: 0;
    color: #707070;
    font-size: 18px;
}

.search_bar .input-group-addon {
    margin: 0 0 0 -27px;
}

.user-info h5 {
    font-size: 15px;
    color: #464646;
    margin: 0 0 8px 0;
}

.user-info h5 span {
    font-size: 13px;
    float: right;
}

.user-info p {
    font-size: 14px;
    color: #989898;
    margin: auto;
}

.user-image {
    float: left;
    width: 11%;
}

.user-info {
    float: left;
    padding: 0 0 0 15px;
    width: 88%;
}

.user {
    overflow: hidden;
    clear: both;
}

.user-container {
    border-bottom: 1px solid #c4c4c4;
    margin: 0;
    padding: 18px 16px 10px;
}

.users-container {
    height: 550px;
    overflow-y: scroll;
}

.active_chat {
    background: #ebebeb;
}

.received_msg {
    display: inline-block;
    padding: 0 0 0 10px;
    vertical-align: top;
    width: 92%;
}

.received_withd_msg p {
    background: #ebebeb none repeat scroll 0 0;
    border-radius: 3px;
    color: #646464;
    font-size: 14px;
    margin: 0;
    padding: 5px 10px 5px 12px;
    width: 100%;
}

.time_date {
    color: #747474;
    display: block;
    font-size: 12px;
    margin: 8px 0 0;
}

.received_withd_msg {
    width: 57%;
}

.right-container {
    float: left;
    padding: 30px 15px 0 25px;
    width: 60%;
}

.sent_msg p {
    background: #05728f none repeat scroll 0 0;
    border-radius: 3px;
    font-size: 14px;
    margin: 0;
    color: #fff;
    padding: 5px 10px 5px 12px;
    width: 100%;
}

.outgoing_msg {
    overflow: hidden;
    margin: 26px 0 26px;
}

.sent_msg {
    float: right;
    width: 46%;
}

.input_msg_write input {
    background: rgba(0, 0, 0, 0) none repeat scroll 0 0;
    border: medium none;
    color: #4c4c4c;
    font-size: 15px;
    min-height: 48px;
    width: 100%;
}

.chat-message-input-container {
    border: 1px solid #c4c4c4;
    position: relative;
}

.msg_send_btn {
    cursor: pointer;
    font-size: 17px;
    height: 33px;
    position: absolute;
    right: 0;
    top: 6px;
    width: 33px;
    margin-right: 5px;
}

.messaging {
    padding: 0 0 50px 0;
}

.write_msg {
    padding-left: 10px;
}

.chat-message-container {
    height: 516px;
    overflow-y: auto;
}

@media only screen and (max-width: 500px) {
    .incoming_msg_img {
        display: none;
    }

    .user-image {
        display: none;
    }

    .user-info h5 {
        font-size: 10px;
    }

    .sent_msg p,
    .received_msg p {
        font-size: 10px;
    }

    .time_date {
        font-size: 8px;
    }

    .msg_send_btn {
        display: none;
    }
}
</style>
