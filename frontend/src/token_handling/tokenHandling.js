import { jwtDecode } from "jwt-decode";

function decodeToken(token) {
    try {
        const decodedToken = jwtDecode(token)
        return decodedToken
    } catch (error) {
        console.error('JWT verification failed:', error.message);
        return null
    }
} 

export default decodeToken;


