<template>
    <v-container id="signinup-form" class="fill-height">
        <notifications group="loginfail" position="bottom center" />
        <notifications group="signupfail" position="bottom center" />
        <v-row align="center" justify="center" no-gutters>
            <v-col cols="12" sm="8" md="8" class="">
                <v-card class="evelation-12 card">
                    <v-window v-model="step">
                        <!--SignIn-->
                        <v-window-item :value="1">
                            <v-row class="">
                                <v-col cols="12" md="8" class="pt-6 pb-6">
                                    <v-card-text>
                                        <v-form class="signup-form-form" @submit.prevent="signin">
                                            <h1
                                                class="text-center display-1 mb-10"
                                                :class="`${bgColor}--text`"
                                            >
                                                Sign in
                                            </h1>
                                            <v-text-field
                                                id="username"
                                                v-model="login"
                                                label="Username"
                                                name="Username"
                                                type="text"
                                                :color="bgColor"
                                            />
                                            <v-text-field
                                                id="password"
                                                v-model="password"
                                                label="Password"
                                                name="Password"
                                                type="password"
                                                :color="bgColor"
                                            />
                                            <div class="text-center mt-6">
                                                <v-btn type="submit" large :color="bgColor" dark
                                                    >Sign In
                                                </v-btn>
                                            </div>
                                        </v-form>
                                    </v-card-text>
                                </v-col>
                                <v-col
                                    cols="12"
                                    md="4"
                                    class="darken-2 vcenter"
                                    :class="`${bgColor}`"
                                >
                                    <div>
                                        <v-card-text :class="`${fgColor}--text`">
                                            <h1 class="text-center headline mb-3">Not a User?</h1>
                                            <h5 class="text-center overline mb-3">
                                                Please Sign Up to continue
                                            </h5>
                                        </v-card-text>
                                        <div class="text-center mb-6">
                                            <v-btn dark outlined @click="step = 2">Sign Up</v-btn>
                                        </div>
                                    </div>
                                </v-col>
                            </v-row>
                        </v-window-item>
                        <!--SignUp-->
                        <v-window-item :value="2">
                            <v-row class="fill-height">
                                <v-col
                                    cols="12"
                                    md="4"
                                    class="darken-2 vcenter"
                                    :class="`${bgColor}`"
                                >
                                    <div>
                                        <v-card-text :class="`${fgColor}--text`">
                                            <h1 class="text-center headline mb-3">
                                                Already a user?
                                            </h1>
                                            <h5 class="text-center overline mb-3">
                                                Please Sign In
                                            </h5>
                                        </v-card-text>
                                        <div class="text-center mb-6">
                                            <v-btn dark outlined @click="step = 1">Sign In</v-btn>
                                        </div>
                                    </div>
                                </v-col>
                                <v-col cols="12" md="8" class="pt-6 pb-6">
                                    <v-card-text>
                                        <h1
                                            class="text-center display-1 mb-10"
                                            :class="`${bgColor}--text`"
                                        >
                                            Sign Up
                                        </h1>
                                        <v-form class="signup-form-form" @submit.prevent="signup">
                                            <v-text-field
                                                id="username"
                                                v-model="username"
                                                label="Username"
                                                name="username"
                                                type="text"
                                            />
                                            <v-text-field
                                                id="password"
                                                v-model="password"
                                                label="Password"
                                                name="password"
                                                type="password"
                                            />
                                            <v-text-field
                                                id="confirmPassword"
                                                v-model="confirmPassword"
                                                label="Confirm Password"
                                                name="confirmPassword"
                                                type="password"
                                            />
                                            <div class="text-center mt-6">
                                                <v-btn type="submit" large :color="bgColor" dark>
                                                    Sign Up
                                                </v-btn>
                                            </div>
                                        </v-form>
                                    </v-card-text>
                                </v-col>
                            </v-row>
                        </v-window-item>
                    </v-window>
                </v-card>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
export default {
    // Different layout compared to default
    head: {
        title: "Vueducation - Login",
    },
    layout: "landing",
    props: {
        source: {
            type: String,
            default: "",
        },
        bgColor: {
            type: String,
            default: "indigo",
        },
        fgColor: {
            type: String,
            default: "white",
        },
    },

    data: () => ({
        step: 1,
        username: "",
        email: "",
        password: "",
        confirmPassword: "",
        login: "",
        error: "",
    }),

    methods: {
        async signin() {
            try {
                const response = await this.$auth.loginWith("local", {
                    data: {
                        username: this.login,
                        password: this.password,
                    },
                });
            } catch (err) {
                this.notify();
                // Reset password placeholder
                this.password = "";
            }
        },

        async signinFromSingup() {
            try {
                const response = await this.$auth.loginWith("local", {
                    data: {
                        username: this.username,
                        password: this.password,
                    },
                });
            } catch (err) {
                this.notify();
                this.password = "";
            }
        },

        async signup() {
            if (this.password !== this.confirmPassword) {
                this.notifySignUp();
            } else {
                const data = {
                    username: this.username,
                    password: this.password,
                };

                const that = this;
                this.$axios.post("/api/auth/signup", data).then(function (response) {
                    // Create conversation empty record in Firebase
                    that.$fire.firestore.collection("conversation").doc(that.username).set({
                        friends: [],
                    });
                    that.signinFromSingup();
                });
            }
        },

        notify() {
            this.$notify({
                group: "loginfail",
                title: "Login Attempt",
                text: "Credential is invalid!",
                type: "error",
            });
        },

        notifySignUp() {
            this.$notify({
                group: "signupfail",
                title: "Signup Attempt",
                text: "Password mismatch!",
                type: "error",
            });
        },
    },
};
</script>

<style scoped lang="scss">
.v-input__icon--double .v-input__icon {
    margin-left: -4.25rem !important;
}
a.no-text-decoration {
    text-decoration: none;
}
#signinup-form {
    max-width: 75rem;
}
.signup-form-form {
    max-width: 23rem;
    margin: 0 auto;
}
.card {
    overflow: hidden;
}
.vcenter {
    display: flex;
    align-items: center;
    justify-content: center;
}
</style>
