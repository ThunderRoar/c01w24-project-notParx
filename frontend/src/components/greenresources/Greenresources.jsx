import './Greenresources.scss';
import "leaflet/dist/leaflet.css"
import React from 'react';
import { useState, useEffect } from 'react';
import { MapContainer, TileLayer, useMap, Marker, useMapEvents, Popup } from "react-leaflet";
import axios from 'axios';


const GreenResources = () => {
    const [position, setPosition] = useState(null)
    const [parks, setParks] = useState([]);

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


    return (
        <div className='map-component'>
            <div className='service-header'>Green Resources</div>
            <div className='content'>
                <div className='nav'>
                    <div className='map-filter'>
                        <button>Filter</button>
                    </div>

                    <div className='map-search-bar'>
                        <input type="text" placeholder="Search Here..." />
                    </div>

                    <div className='map-find-button'>
                        <button>Search</button>
                    </div>
                </div>
                <div className='map-container'>
                    <MapContainer center={[43.65, -79.39]} zoom={12} scrollWheelZoom={true}>
                        <TileLayer 
                            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                            url='https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'
                        />
                        
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