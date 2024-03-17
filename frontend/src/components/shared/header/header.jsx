import React, { useState, useEffect } from 'react';
import './header.scss';
import logoImg from '../../../resources/img/parx_logo.png';
import AccountIcon from '@mui/icons-material/AccountCircleOutlined';
import Tab from './tabs/Tabs';

const Header = ({ tabs }) => {

    const activeTab = 'hi';

    const handleTabClick = (tabTitle) => {
        console.log('hi');
    };

    const logoImgLink = logoImg;

    return (
        <div className='header'> 
            <div className='nav'>
                <img className='logo' src={logoImgLink} />
                {tabs.length > 0 && (
                    <div className='page-links'>
                        {tabs.map((tab) => (
                            <Tab 
                                key={tab.id}
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