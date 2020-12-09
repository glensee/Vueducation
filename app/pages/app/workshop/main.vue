<template>
    <div id="workshop-top">
        <div class="text-md-h3 text-sm-h4 text-lg-h2 font-weight-medium mt-5">
            Recommended Workshops
        </div>

        <v-container fluid class="mb-5">
            <v-row align="start" v-if="isLoading">
                <v-col v-for="index in 4" :key="index">
                    <v-card md="3">
                        <v-skeleton-loader type="card-avatar"></v-skeleton-loader>
                    </v-card>
                </v-col>
            </v-row>

            <v-row align="start" v-if="isLoading == false">
                <v-carousel hide-delimiters>
                    <v-carousel-item
                        v-for="item in recommendedRows"
                        :key="item.index"
                        :src="item.img"
                        @click="$router.push(`/app/workshop/${item.index}`)"
                        style="cursor: pointer"
                    >
                        <v-row class="fill-height" align="center" justify="center">
                            <!-- <div class="display-3">{{ item.title }}</div> -->
                            <div>
                                <v-col>
                                    <v-row class="mb-3">
                                        <div
                                            class="display-3 font-weight-medium"
                                            id="carousel-title"
                                        >
                                            {{ item.title }}
                                        </div>
                                    </v-row>
                                    <v-row>
                                        <div
                                            class="display-1 font-weight-medium"
                                            id="carousel-title"
                                        >
                                            {{ item.institution }}
                                        </div>
                                    </v-row>
                                </v-col>
                            </div>
                        </v-row>
                    </v-carousel-item>
                </v-carousel>
            </v-row>
        </v-container>

        <v-container fluid>
            <span class="text-md-h3 text-sm-h4 text-lg-h2 font-weight-medium mt-5"
                >All Workshops</span
            >
            <v-row align="center">
                <v-col cols="12">
                    <v-skeleton-loader type="text" v-if="isLoading"></v-skeleton-loader>
                    <v-autocomplete
                        v-model="selectedCategories"
                        :items="categories"
                        multiple
                        label="Categories"
                        chips
                        clearable
                        onchange
                        v-if="isLoading == false"
                        style="margin: 0px auto"
                    >
                    </v-autocomplete>
                </v-col>
            </v-row>
        </v-container>

        <v-container fluid v-if="isLoading">
            <v-row align="start" v-for="j in 2" :key="j">
                <v-col v-for="index in 4" :key="index">
                    <v-card md="3">
                        <v-skeleton-loader type="card-avatar"></v-skeleton-loader>
                    </v-card>
                </v-col>
            </v-row>
        </v-container>
        <v-container fluid v-if="isLoading == false">
            <v-row align="center">
                <v-col md="6" sm="12" lg="3" v-for="row in filteredWorkshops()" :key="row.index">
                    <v-card style="cursor: pointer" @click="$router.push(`/app/workshop/${row.index}`)">
                        <v-img
                            :src="row.img"
                            max-width="100%"
                            max-height="200px"
                            style="margin: auto"
                        />
                        <v-card-text>
                            <v-chip color="primary" style="font-size: 10px">{{
                                row.category
                            }}</v-chip>
                            <v-chip color="secondary" style="font-size: 10px">{{
                                row.mode
                            }}</v-chip>
                        </v-card-text>

                        <v-card-title primary-title>
                            {{ row.title }}
                        </v-card-title>

                        <v-card-subtitle>
                            {{ row.institution }}
                        </v-card-subtitle>

                        <v-card-text>
                            {{
                                row.description.length > maxDescriptionLength
                                    ? row.description.substring(0, maxDescriptionLength) +
                                      " more..."
                                    : row.description
                            }}
                        </v-card-text>
                    </v-card>
                </v-col>
            </v-row>
        </v-container>

        <v-btn fab dark large color="primary" fixed right bottom to="/app/workshop/create">
            <v-icon>mdi-plus</v-icon>
        </v-btn>
    </div>
</template>

<script>
export default {
    head: {
        title: `Vueducation - Workshop`,
    },
    data: () => ({
        isLoading: true,
        maxDescriptionLength: 75,
        recommendedRows: [],
        workshops: [],
        categories: [],
        selectedCategories: [],
    }),

    middleware: ["auth"],

    methods: {
        filteredWorkshops() {
            var x = this.workshops.filter((ws) => {
                return (
                    this.selectedCategories.length == 0 ||
                    this.selectedCategories.includes(ws.category)
                );
            });

            return x;
        },
    },

    mounted() {
        fetch(process.env.NUXT_ENV_BACKEND + "/getWorkshops")
            .then((resp) => {
                if (!resp.ok) {
                    throw Error(resp.statusText);
                }
                return resp;
            })
            .then((resp) => resp.json())
            .then((data) => {
                this.workshops = data;
                var tempSet = new Set();
                data.map((obj) => {
                    tempSet.add(obj.category);
                });
                this.categories = Array.from(tempSet);
            })
            .catch((err) => console.log("oops Workshops API is down", err));

        fetch(process.env.NUXT_ENV_BACKEND + "/getRecommended")
            .then((resp) => {
                if (!resp.ok) {
                    throw Error(resp.statusText);
                } else {
                    return resp;
                }
            })
            .then((resp) => resp.json())
            .then((data) => {
                this.recommendedRows = data;

                this.isLoading = false;
            })
            .catch((err) => console.log("oops Workshops API is down", err));
    },
};
</script>

<style>
#workshop-top {
    width: 90%;
    margin: auto;
}

#carousel-title {
    -webkit-text-stroke-width: 1px;
    -webkit-text-stroke-color: black;
}
</style>
