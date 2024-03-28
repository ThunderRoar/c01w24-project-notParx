import './Greenresources.scss';
import "leaflet/dist/leaflet.css";
import educationBuilding from '../../resources/img/university_icon.png';
import natureReserve from '../../resources/img/nature_reserve.png';
import parkIcon from '../../resources/img/park_icon.png';
import dogParkIcon from '../../resources/img/dogParkicon.png';
import gardenIcon from '../../resources/img/gardenIcon.png';
import homeIcon from '../../resources/img/homeIcon.png';
import curIcon from '../../resources/img/placeholder.png';
import earthGIF from '../../resources/img/earth.gif'
import golf from '../../resources/img/golfIcon.png'
import fish from '../../resources/img/fishingIcon.png'
import wildlife from '../../resources/img/wildLifeIcon.png'

import React from 'react';
import { useState, useEffect } from 'react';

import { MapContainer, TileLayer, useMap, Marker, useMapEvents, Popup } from "react-leaflet";
import "leaflet-control-geocoder/dist/Control.Geocoder.css";
import "leaflet-control-geocoder/dist/Control.Geocoder.js";

import MarkerClusterGroup from 'react-leaflet-cluster';
import L, { Icon, divIcon, icon } from "leaflet";
import axios from 'axios';

import LeafletControlGeocoder from './LeafletControlGeocoder';

const GreenResources = (props) => {
    const [position, setPosition] = useState(null);
    
    const [parks, setParks] = useState([]);
    const [selectedOption, setSelectedOption] = useState('park');
    const [selectedISO, setSelectedISO] = useState('1');
    const [region, setRegion] = useState('CA');
    const [adminLevel, setAdminLevel] = useState('2');

    const UniversityIcon = new Icon({
        iconUrl: educationBuilding,
        iconSize: [30, 30],
        popupAnchor:  [-0, -0],
    });

    const HomeIcon = new Icon({
        iconUrl: homeIcon,
        iconSize: [30, 30],
        popupAnchor:  [-0, -0],
    });

    const CurrentLocation = new Icon({
        iconUrl: curIcon,
        iconSize: [30, 30],
        popupAnchor:  [-0, -0],
    });

    const NatureReserve = new Icon({
        iconUrl: natureReserve,
        iconSize: [30, 30],
        popupAnchor:  [-0, -0],
    });

    const ParkIcon = new Icon({
        iconUrl: parkIcon,
        iconSize: [30, 30],
        popupAnchor:  [-0, -0],
    });

    const DogParkIcon = new Icon({
        iconUrl: dogParkIcon,
        iconSize: [30, 30],
        popupAnchor:  [-0, -0],
    });

    const GardenIcon = new Icon({
        iconUrl: gardenIcon,
        iconSize: [30, 30],
        popupAnchor:  [-0, -0],
    });

    const FishingIcon = new Icon({
        iconUrl: fish,
        iconSize: [30, 30],
        popupAnchor:  [-0, -0],
    });

    const GolfIcon = new Icon({
        iconUrl: golf,
        iconSize: [30, 30],
        popupAnchor:  [-0, -0],
    });

    const WildlifeIcon = new Icon({
        iconUrl: wildlife,
        iconSize: [30, 30],
        popupAnchor:  [-0, -0],
    });

    const iconMappings = {
        'nature_reserve': NatureReserve,
        'garden': GardenIcon,
        'park': ParkIcon,
        'dog_park': DogParkIcon,
        'home': HomeIcon,
        'golf_course': GolfIcon,
        'fishing': FishingIcon,
        'wildlife_hide': WildlifeIcon,
        'university': UniversityIcon,
        "current": CurrentLocation,
    };

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await axios.get('https://overpass-api.de/api/interpreter', {
                    params: {
                        data: `[out:json];
                                area["ISO3166-1"="CA"][admin_level=2];
                                (
                                    node["leisure"="park"](area);
                                    way["leisure"="park"](area);
                                    relation["leisure"="park"](area);
                                );
                                out body;
                                >;
                                out skel qt;`,
                    }
                });
                setParks(response.data.elements);
                console.log(response.data.elements);
            } catch (error) {
                console.error('Error fetching park data:', error);
            }
        };

        fetchData();
    }, []);

    useEffect(() => {
        const fetchData = async () => {
            console.log(selectedOption, selectedISO, region, adminLevel);
            try {
                const response = await axios.get('https://overpass-api.de/api/interpreter', {
                    params: {
                        data: `[out:json];
                                area["ISO3166-${selectedISO}"="${region}"][admin_level=${adminLevel}];
                                (
                                    node["leisure"="${selectedOption.toLowerCase()}"](area);
                                    way["leisure"="${selectedOption.toLowerCase()}"](area);
                                    relation["leisure"="${selectedOption.toLowerCase()}"](area);
                                );
                                out body;
                                >;
                                out skel qt;`,
                    }
                });
                setParks(response.data.elements);
                // console.log(response.data.elements);
            } catch (error) {
                console.error('Error fetching park data:', error);
            }
        };
    
        fetchData();
    }, [selectedOption, selectedISO, region, adminLevel]);
    


    const handleThemeChange = (e) => {
        setSelectedOption(e.target.value);
    }

    const handleFilterChange = (e) => {
        setRegion(e.target.value);
        
        if (e.target.value === "CA") {
            setSelectedISO("1");
            setAdminLevel("2");
        } else {
            setSelectedISO("2");
            setAdminLevel("4");
        }
    }

    function LocationMarker() {
        const map = useMapEvents({
          click() {
            map.locate()
          },
          locationfound(e) {
            setPosition(e.latlng)
            map.flyTo(e.latlng, map.getZoom())
          },
        })
      
        return position === null ? null : (
          <Marker position={position} icon={iconMappings['home']}>
            <Popup>You are here</Popup>
          </Marker>
        )
    }

    return (
        <div className='map-component'>
            {/* <div className='service-header'>Green Resources</div> */}
            <div className='content'>
                <div className='nav'>
                    <div className='map-filter-theme'>
                        
                        <div className='filter-heading'>Filter:</div>
                        <select onChange={handleThemeChange}>
                            <option value={"park"}>Park</option>
                            <option value={"nature_reserve"}><image></image>Nature Reserve</option>
                            <option value={"garden"}>Garden</option>
                            <option value={"dog_park"}>Dog Park</option>
                            <option value={"fishing"}>Fishing</option>
                            <option value={"golf_course"}>Golf Course</option>
                            <option value={"wildlife_hide"}>Wildlife Hide</option>
                        </select>

                    </div>

                    <div className='map-title'>
                        Green Resources         
                    </div>

                    <div className='map-filter-region'>
                        <div className='region-heading'>Region:</div>
                        <select onChange={handleFilterChange}>
                            {/* Need ISO to be 1 and admin level to 2 for canada and for prov, need ISO to be 2 and amdin level to be 4 */}
                            <option value={"CA"}>Canada</option> 
                            <option value={"CA-ON"}>Ontario</option>
                            <option value={"CA-AB"}>Alberta</option>
                            <option value={"CA-BC"}>British Columbia</option>
                            <option value={"CA-MB"}>Manitoba</option>
                            <option value={"CA-NB"}>New Brunswick</option>
                            <option value={"CA-NL"}>Newfoundland and Labrador</option>
                            <option value={"CA-NS"}>Nova Scotia</option>
                            <option value={"CA-PE"}>Prince Edward Island</option>
                            <option value={"CA-QC"}>Quebec</option>
                            <option value={"CA-SK"}>Saskatchewan</option>
                            <option value={"CA-NT"}>Northwest Territories</option>
                            <option value={"CA-NU"}>Nunavut</option>
                            <option value={"CA-YT"}>Yukon</option>
                        </select>

                    </div>
                </div>
                <div className='map-container'>
                    <MapContainer center={[43.7830999, -79.189901]} zoom={12} scrollWheelZoom={true}>
                        <TileLayer 
                            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                            url='https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'
                        />

                        <Marker position={[43.7830999, -79.189901]} icon={iconMappings['university']}>
                            <Popup>
                                UTSC
                            </Popup>
                        </Marker>
                        
                        {/* Use the below if user wants to know where they are currenly */}
                        <LocationMarker/>
                        <LeafletControlGeocoder/>
                        

                        <MarkerClusterGroup 
                            chunkedLoading
                        >
                            {parks.map(park => (
                                <Marker key={park.id} position={[park.lat, park.lon]} icon={iconMappings[selectedOption]}>
                                    <Popup>{park.tags.name}</Popup>
                                </Marker>
                            ))}
                        </MarkerClusterGroup>
                        
                    </MapContainer>
                </div>
            </div>
            <section>
                <img className="earth-revolving-sustainability" src={earthGIF} alt="earth revolving" />
            </section>
        </div>
    );
};

export default GreenResources;


