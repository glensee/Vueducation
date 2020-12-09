<template>
    <v-container width="50">
        <v-row no-gutters class="pt-4">
            <v-flex xs12 md4 class="pr-4">
                <v-img
                    lazy-src="https://static.ricemedia.co/wp-content/uploads/2018/11/Rice-Media-PSLE-Grades-Singapore-Education-System-Leaders-Followers-1-1024x683.jpg"
                    max-height="250"
                    max-width="350"
                    src="https://static.ricemedia.co/wp-content/uploads/2018/11/Rice-Media-PSLE-Grades-Singapore-Education-System-Leaders-Followers-1-1024x683.jpg"
                ></v-img>
                <h4 class="mt-4">Created by students, for students.</h4>
                <div>
                    We are dedicated to bringing back personalised learning to every student. We
                    rely on donations and advertisements to carry out our mission to keep student
                    discussions alive and open.
                </div>
                <h4>Will you give today?</h4>
                <br />
            </v-flex>
            <v-flex>
                <v-card>
                    <v-tabs color="primary accent-4" left>
                        <v-tab>Donate now</v-tab>
                        <v-tab>Advertisements</v-tab>

                        <v-tab-item>
                            <v-container fluid>
                                <donateForm />
                            </v-container>
                        </v-tab-item>

                        <v-tab-item>
                            <v-carousel :show-arrows="true" hide-delimiters>
                                <v-carousel-item>
                                    <v-row class="fill-height pa=0" align="center" justify="center">
                                        <client-only placeholder="Loading...">
                                            <youtube
                                                :video-id="'x7mAFcNc85E'"
                                                class="text-center"
                                            ></youtube>
                                        </client-only>
                                    </v-row>
                                </v-carousel-item>
                                <v-carousel-item>
                                    <v-row class="fill-height pa=0" align="center" justify="center">
                                        <client-only placeholder="Loading...">
                                            <youtube
                                                :video-id="'2XAGCZ3Sg4o'"
                                                class="text-center"
                                            ></youtube>
                                        </client-only>
                                    </v-row>
                                </v-carousel-item>
                                <v-carousel-item>
                                    <v-row class="fill-height pa=0" align="center" justify="center">
                                        <client-only placeholder="Loading...">
                                            <youtube
                                                :video-id="'wK2B4NWwS0w'"
                                                class="text-center"
                                            ></youtube>
                                        </client-only>
                                    </v-row>
                                </v-carousel-item>
                            </v-carousel>
                        </v-tab-item>
                    </v-tabs>
                </v-card>
            </v-flex>
        </v-row>
    </v-container>
</template>

<script>
import donateForm from "../../components/donateForm";

export default {
    head: {
        title: "Vueducation - Donate",
    },
    components: {
        donateForm,
    },
    middleware: ["auth"],
};
</script>
<style></style>
