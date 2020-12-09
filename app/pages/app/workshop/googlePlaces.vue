<template>
    <div>
        <v-text-field
            outlined
            clearable
            label="Enter a location"
            id="searchTextField"
            :required="getMode() == 'physical' && getMode() != undefined"
        ></v-text-field>

        <div
            id="gmap"
            style="height: 300px; margin-bottom: 32px"
            :class="lat == 0 && lng == 0 ? `hide-map` : ``"
        ></div>
    </div>
</template>

<script>
export default {
    head() {
        return {
            script: [
                {
                    src: `https://maps.googleapis.com/maps/api/js?key=${process.env.NUXT_ENV_GOOGLE_API}&region=SG&libraries=places`,
                },
            ],
        };
    },
    middleware: ["auth"],
    data() {
        return {
            searchField: "",
            lat: 0,
            lng: 0,
        };
    },

    props: {
        parentMode: {
            type: String,
            required: true,
        },
    },

    methods: {
        getMode() {
            return this.parentMode;
        },
        refreshMap() {
            var myLatLng = { lat: this.lat, lng: this.lng };
            var map = new google.maps.Map(document.getElementById("gmap"), {
                zoom: 17,
                center: myLatLng,
            });

            var map = new google.maps.Marker({
                position: myLatLng,
                map,
                title: "Workshop location",
            });
        },
    },

    mounted() {
        console.log(this.getMode() == "physical" && this.getMode() != undefined);
        const root = this;
        // var input = this.$refs.searchTextField; //.getElementById('searchTextField');
        var input = document.getElementById("searchTextField");
        var autocomplete = new google.maps.places.Autocomplete(input);
        google.maps.event.addListener(autocomplete, "place_changed", function () {
            var place = autocomplete.getPlace();
            root.searchField = place.formatted_address;
            root.lat = place.geometry.location.lat();
            root.lng = place.geometry.location.lng();
            root.$emit("getLatLng", {
                lat: place.geometry.location.lat(),
                lng: place.geometry.location.lng(),
            });
            root.refreshMap();
        });
    },
};
</script>

<style>
.hide-map {
    display: none;
}
</style>
