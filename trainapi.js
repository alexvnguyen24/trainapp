import express from 'express';

const app = express();
const PORT = process.env.PORT || 3000; // Use environment variable or default to 3000
const APIKEY = "0bb673745a154df0a0d7363a97d41d1a";
const URL = "https://api-v3.mbta.com";

// Get red line information
app.get('/red', async (req, res) => {
    try{
        const response = await fetch(`${URL}/vehicles?filter[route]=Red`, {
            headers: {
                'X-Api-Key': APIKEY
            }
        });
        
        if(!response.ok){
            throw new Error(`API request failed with status: ${response.status} in /red`);
        }

        const trainInfo = await response.json();
        const trainData = trainInfo["data"];
        res.send(Object.values(trainData).filter(obj => obj.attributes.current_status === "STOPPED_AT"));
    }
    catch(error){
        console.error(`${error} in /red`);
        res.status(500).json({error: error.message});
    }
});

// Get blue line information
app.get('/blue', async (req, res) => {
    try{
        const response = await fetch(`${URL}/vehicles?filter[route]=Blue`, {
            headers: {
                'X-Api-Key': APIKEY
            }
        });
        
        if(!response.ok){
            throw new Error(`API request failed with status: ${response.status} in /blue`);
        }

        const trainInfo = await response.json();
        const trainData = trainInfo["data"];
        res.send(Object.values(trainData).filter(obj => obj.attributes.current_status === "STOPPED_AT"));
    }
    catch(error){
        console.error(`${error} in /blue`);
        res.status(500).json({error: error.message});
    }
});

// Get specific stop information
app.get('/stop/:id', async (req, res) => {
    try{
        const response = await fetch(`${URL}/stops`, {
            headers: {
                'X-Api-Key': APIKEY
            }
        });

        const id = req.params.id;
        
        if(!response.ok){
            throw new Error(`API request failed with status: ${response.status}`);
        }

        const stopInfo = await response.json();
        const stopData = stopInfo["data"];
        res.send(Object.values(stopData).find(obj => obj.id === id));
        return Object.values(stopData).find(obj => obj.id === id);
    }
    catch(error){
        console.error(error);
        res.status(500).json({error: error.message});
    }
});

// Get list of stops
app.get('/stops', async (req, res) => {
    try{
        const response = await fetch(`${URL}/stops`, {
            headers: {
                'X-Api-Key': APIKEY
            }
        });
        
        if(!response.ok){
            throw new Error(`API request failed with status: ${response.status}`);
        }

        const stopInfo = await response.json();
        res.send(stopInfo);
    }
    catch(error){
        console.error(error);
        res.status(500).json({error: error.message});
    }
});

// Dummy route
app.get('/test', async (req, res) => {
    try{
        const response = await fetch(`${URL}/vehicles?filter[route]=116`, {
            headers: {
                'X-Api-Key': APIKEY
            }
        });
        
        if(!response.ok){
            throw new Error(`API request failed with status: ${response.status}`);
        }

        const trainInfo = await response.json();
        const trainData = trainInfo["data"];
        res.send(Object.values(trainData).filter(obj => obj.attributes.current_status === "STOPPED_AT"));
        //res.send(trainInfo);
    }
    catch(error){
        console.error(error);
        res.status(500).json({error: error.message});
    }
});

app.get('/t', async (req, res) => {
    try{
        const response = await fetch(`${URL}/routes`, {
            headers: {
                'X-Api-Key': APIKEY
            }
        });
        
        if(!response.ok){
            throw new Error(`API request failed with status: ${response.status}`);
        }

        const trainInfo = await response.json();
        const stopData = trainInfo["data"];
        //res.send(Object.values(stopData).find(obj => obj.id === "7954"));
        res.send(stopData);
        //Object.values(stopData).find(obj => obj.id === "7954");
    }
    catch(error){
        console.error(error);
        res.status(500).json({error: error.message});
    }
});

app.get('/m', async (req, res) => {
    try{
        const response = await fetch(`${URL}/stops?filter[route]=Orange`, {
            headers: {
                'X-Api-Key': APIKEY
            }
        });
        
        if(!response.ok){
            throw new Error(`API request failed with status: ${response.status}`);
        }

        const trainInfo = await response.json();
        const stopData = trainInfo["data"];
        //res.send(Object.values(stopData).find(obj => obj.id === "7954"));
        res.send(stopData);
        //Object.values(stopData).find(obj => obj.id === "7954");
    }
    catch(error){
        console.error(error);
        res.status(500).json({error: error.message});
    }
});

// Start the server
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
