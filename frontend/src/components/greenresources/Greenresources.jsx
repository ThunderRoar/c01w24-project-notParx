import './Greenresources.scss';
import "leaflet/dist/leaflet.css";
import educationBuilding from '../../resources/img/university_icon.png';
import React from 'react';
import { useState, useEffect } from 'react';
// import { GoogleMap, Marker, InfoWindow, useLoadScript } from '@react-google-maps/api';
// import { formatRelative } from "date-fns";
import { MapContainer, TileLayer, useMap, Marker, useMapEvents, Popup } from "react-leaflet";
import L from "leaflet";
import axios from 'axios';


const GreenResources = () => {
    // const [mapCenter, setMapCenter] = ([43.7830999, -79.189901]);
    // const [mapZoom, setMapZoom] = (12);
    const [position, setPosition] = useState(null)
    const [parks, setParks] = useState([]);
    const [filteredParks, setFilteredParks] = useState([]);
    const [searchQuery, setSearchQuery] = useState('');
    const [region, setRegion] = useState('');
    const [selectedOption, setSelectedOption] = useState('Nature Reserve');

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
                console.log(selectedOption);
            } catch (error) {
                console.error('Error fetching park data:', error);
            }
        };

        fetchData();
    }, [selectedOption]);

    useEffect(() => {
        const filter = parks.filter(park => {
            if (region && park.tags.name && park.tags.name.toLowerCase().includes(region.toLowerCase())) {
                return true;
            }

            // If user has searched something
            if (searchQuery) {
                const searchReq = searchQuery.toLowerCase().split(' ');
                return searchReq.some(term => park.tags.name.toLowerCase().includes(term));
            }
            return true;
        })
        setFilteredParks(filter);
    }, [parks, searchQuery, region]);

    const handleSearchChange = (e) => {
        setSearchQuery(e.target.value);
    }

    const handleFilterChange = (e) => {
        setSelectedOption(e.target.value);
    }

    const handleRegionChange = (e) => {
        setRegion(e.target.value);
    }

    // const handleMapClick = (e) => {
    //     setPosition(e.latlng);
    // }


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
          <Marker position={position}>
            <Popup>You are here</Popup>
          </Marker>
        )
    }

    const universityIcon = L.icon({
        iconUrl: educationBuilding,
        iconSize: [30, 30],
        popupAnchor:  [-0, -0],
    });

    // const parkIcon = L.icon({
    //     iconUrl: educationBuilding,
    //     iconSize: [30, 30],
    //     popupAnchor:  [-0, -0],
    // });

    return (
        <div className='map-component'>
            <div className='service-header'>Green Resources</div>
            <div className='content'>
                <div className='nav'>
                    <div className='map-filter'>
                        
                        <select onChange={handleFilterChange}>
                            <option>Nature Reserve</option>
                            <option>Garden</option>
                            <option>Park</option>
                            <option>Dog Park</option>
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

                        <Marker position={[43.7830999, -79.189901]} icon={universityIcon}>
                            <Popup>
                                UTSC
                            </Popup>
                        </Marker>
                        
                        {/* Use the below if user wants to know where they are currenly
                        <LocationMarker/> */}

                        {parks.map(park => (
                            <Marker key={park.id} position={[park.lat, park.lon]}>
                                <Popup>{park.tags.name}</Popup>
                            </Marker>
                        ))}
                    </MapContainer>
                </div>
            </div>
        </div>
    );
};

export default GreenResources;


