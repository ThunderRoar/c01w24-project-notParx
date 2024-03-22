import './Greenresources.scss';
import "leaflet/dist/leaflet.css";
import educationBuilding from '../../resources/img/university_icon.png';
import natureReserve from '../../resources/img/nature_reserve.png';
import parkIcon from '../../resources/img/park_icon.png';
import dogParkIcon from '../../resources/img/dogParkicon.png';
import gardenIcon from '../../resources/img/gardenIcon.png';
import homeIcon from '../../resources/img/homeIcon.png';
import curIcon from '../../resources/img/placeholder.png';

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

    const [filteredParks, setFilteredParks] = useState([]);
    const [searchQuery, setSearchQuery] = useState('');
    const [region, setRegion] = useState('');


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

    const iconMappings = {
        'nature_reserve': NatureReserve,
        'garden': GardenIcon,
        'park': ParkIcon,
        'dog_park': DogParkIcon,
        'home': HomeIcon,
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

    const userSelection = () => {
        const fetchData = async () => {
            try {
                const response = await axios.get('https://overpass-api.de/api/interpreter', {
                    params: {
                        data: `[out:json];
                                area["ISO3166-1"="CA"][admin_level=2];
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
                console.log(response.data.elements);
            } catch (error) {
                console.error('Error fetching park data:', error);
            }
        };

        fetchData();
    };

    // useEffect(() => {
    //     const filter = parks.filter(park => {
    //         if (region && park.tags.name && park.tags.name.toLowerCase().includes(region.toLowerCase())) {
    //             return true;
    //         }

    //         // If user has searched something
    //         if (searchQuery) {
    //             const searchReq = searchQuery.toLowerCase().split(' ');
    //             return searchReq.some(term => park.tags.name.toLowerCase().includes(term));
    //         }
    //         return true;
    //     })
    //     setFilteredParks(filter);
    // }, [parks, searchQuery, region]);

    const handleSearchChange = (e) => {
        console.log(e.target.value);
        setSearchQuery(e.target.value);
    }

    const handleFilterChange = (e) => {
        console.log(e.target.value);
        setSelectedOption(e.target.value);
        userSelection();
    }

    const handleRegionChange = (e) => {
        setRegion(e.target.value);
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
            <div className='service-header'>Green Resources</div>
            <div className='content'>
                <div className='nav'>
                    <div className='map-filter'>
                        
                        <select onChange={handleFilterChange}>
                            <option value={"park"}>Park</option>
                            <option value={"nature_reserve"}><image></image>Nature Reserve</option>
                            <option value={"garden"}>Garden</option>
                            <option value={"dog_park"}>Dog Park</option>
                        </select>

                    </div>

                    <div className='map-search-bar'>
                        <input type='text' placeholder='Search Here...' value={searchQuery} onChange={handleSearchChange} />                       
                    </div>

                    <div className='map-find-button'>
                        <button>Search</button>
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
        </div>
    );
};

export default GreenResources;


