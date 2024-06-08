import { useContext } from 'react';
import { AuthContext } from '../components/AuthContext';

import React from 'react';
import View from '../View';
import Login from './Login';




function Home() {
    const { isLoggedIn } = useContext(AuthContext);

    return (
        <div>
            {isLoggedIn ? (
                <View />
            ) : (
                <Login />
            )}
        </div>
    );
}

export default Home;
