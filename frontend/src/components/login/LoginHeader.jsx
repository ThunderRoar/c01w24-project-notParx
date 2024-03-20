import React from 'react';
import './LoginHeader.scss';
import logoImg from '../../resources/img/parx_logo.png';

const LoginHeader = () => {

    const logoImgLink = logoImg;

    return (
        <div className='header'> 
            <div className='nav'>
                <img className='logo' src={logoImgLink} />
            </div>
        </div>
    );
  };
  
  export default LoginHeader;