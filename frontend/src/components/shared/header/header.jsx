import React, { useState, useEffect } from 'react';
import './header.scss';
import logoImg from '../../../resources/img/parx_logo.png';
import AccountIcon from '@mui/icons-material/AccountCircleOutlined';
import Tab from './tabs/Tabs';
import { useLocation } from 'react-router-dom';

const Header = ({ tabs }) => {

    const activeTab = 'hi';

    // const [activeTab, setActiveTab] = useState(null);

    // const location = useLocation();

    // useEffect(() => {
    //     // Update activeTab when the location (URL) changes
    //     console.log('location changed:', location.pathname); 
    //     console.log('current tabs:', tabs);
    //     const currentPathName = location.pathname.split('/')[1];  // Extract relevant part
    //     const matchingTab = tabs.find(tab => tab.link.split('/')[1] === currentPathName);

    //     if (matchingTab) {
    //         setActiveTab(matchingTab.name);
    //     } 
    //     }, [location, tabs]); // Include 'tabs' in the dependency array

    const handleTabClick = (tabTitle) => {
        console.log('hi');
        // setActiveTab(tabTitle);
    };

    const logoImgLink = logoImg;

    return (
        <div className='header'> 
            <div className='nav'>
                <img className='logo' src={logoImgLink} />
                {tabs.length > 0 && (
                    <div className='page-links'>
                        {tabs.map((tab) => ( // Iterate over the tabs prop
                            <Tab 
                                key={tab.id} // Use unique 'id'
                                title={tab.name}  
                                link={tab.link}
                                isActive={activeTab === tab.name} 
                                onClick={handleTabClick} 
                            />
                        ))}
                    </div>
                )}
            </div>
            <AccountIcon className={`account-icon ${tabs.length > 0 ? '' : 'hide'}`} />
        </div>
    );
  };
  
  export default Header;