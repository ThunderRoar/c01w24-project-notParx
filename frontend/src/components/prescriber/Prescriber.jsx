import React from 'react';
import { prescriberTabs } from '../shared/tabs-data';
import { Outlet } from 'react-router-dom';
import Header from '../shared/header/header';
import "./Prescriber.scss"


const Prescriber = () => {

    const tabs = prescriberTabs;

    return (
        <div className="prescriber-component">
            <Header tabs={tabs} />
            <Outlet />
        </div>
    );
};

export default Prescriber;
