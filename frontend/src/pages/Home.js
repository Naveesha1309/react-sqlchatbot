
import { AuthContext } from '../components/AuthContext';
import React, { useContext, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Login from './Login';
import NavbarLogin from '../components/NavbarLogin';


function Home() {
    const { isLoggedIn } = useContext(AuthContext);
    const navigate = useNavigate();

    useEffect(() => {
        if (isLoggedIn) {
            navigate('/chat');
        }
    }, [isLoggedIn, navigate]);

    return (
        <div>
            <NavbarLogin />
            {!isLoggedIn && <Login />}
        </div>
    );
}

export default Home;
