import { useEffect, useRef } from "react";
import { useMap } from "react-leaflet";
import "leaflet-control-geocoder/dist/Control.Geocoder.css";

import "leaflet-control-geocoder/dist/Control.Geocoder.js";
import L from "leaflet";
import icon from "./constants";

export default function LeafletControlGeocoder({userQuery}) {
  const map = useMap();
  const geocoderRef = useRef(null);

  useEffect(() => {
    if (!geocoderRef.current) {
      var geocoder = L.Control.Geocoder.nominatim();
      if (typeof URLSearchParams !== "undefined" && window.location.search) {
        // parse /?geocoder=nominatim from URL
        var params = new URLSearchParams(window.location.search);
        var geocoderString = params.get("geocoder");
        if (geocoderString && L.Control.Geocoder[geocoderString]) {
          geocoder = L.Control.Geocoder[geocoderString]();
        } else if (geocoderString) {
          console.warn("Unsupported geocoder", geocoderString);
        }
      }

    //   console.log(searchQuery);

      const control = L.Control.geocoder({
        query: "",
        placeholder: "Search here...",
        defaultMarkGeocode: false,
        geocoder
      })
        .on("markgeocode", function (e) {
          var latlng = e.geocode.center;
          L.marker(latlng, { icon })
            .addTo(map)
            .bindPopup(e.geocode.name)
            .openPopup();
          map.fitBounds(e.geocode.bbox);
        })
        .addTo(map);

      geocoderRef.current = control;
    }
  }, [map]);

  return null;
}
