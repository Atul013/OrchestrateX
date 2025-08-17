import React from 'react';
import { Link } from 'react-router-dom';
import './Navbar.css'; // Assuming you have a CSS file for styling the Navbar

const Navbar = () => {
    return (
        <nav className="navbar">
            <div className="navbar-brand">
                <Link to="/">Netflix Clone</Link>
            </div>
            <div className="navbar-links">
                <Link to="/">Home</Link>
                <Link to="/movies">Movies</Link>
                <Link to="/shows">Shows</Link>
                <Link to="/about">About</Link>
            </div>
        </nav>
    );
};

export default Navbar;