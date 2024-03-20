import './LoginBox.scss';
import { Button } from '@mui/material';
import * as React from 'react';
import TablePagination from '@mui/material/TablePagination';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import ReactPopup from 'reactjs-popup';
import axios from 'axios';

const LoginBox = () => {
    return (
        <div className='login-component'>
            <div className='content'>
                <div className='table-container'>
                    <h2>Log in</h2>
                    <p>Who are you?</p>
                    <div className='controls'>                    
                        <p>Patient</p>
                        <p>Prescriber</p>
                        <p>Admin</p>
                    </div>

                    <p>Username</p>
                    <input type="text" className="input-field" placeholder="Username" />
                    <p>Password</p>
                    <input type="text" className="input-field" placeholder="Password" />
                    <div className='row'>
                        <button className='custom-button'>
                            <span>Get Started</span>
                        </button>
                    </div> 
                    


                </div>
            </div>
        </div>
    );
};

export default LoginBox;