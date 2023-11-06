var dataTable = [];

self.onmessage = function(event) {

    let startOfToday = new Date();
    startOfToday.setHours(0, 0, 0, 0);

    dataTable = dataTable.filter(item => new Date(item.timestamp) >= startOfToday);

    if (event.data.type === 'update_data') {
        dataTable = event.data.data; 
    } else if (event.data.type === 'new_data_inserted') {
        dataTable.push(event.data.data);
    }
    
    // Aggregation helper function
    function aggregateByHour(data) {
        let hourlyData = Array(24).fill(0);
        data.forEach(item => {
            let hour = new Date(item.timestamp).getHours(); // Extract the hour
            hourlyData[hour] += item.value;
        });
        return hourlyData.map((value, hour) => ({ x: hour, y: value }));
    }

    let durationData = aggregateByHour(dataTable.filter(item => item.metric === 'duration_at_computer'));
    let keysData = aggregateByHour(dataTable.filter(item => item.metric === 'keys_pressed'));

    let durationPlotData = [{
        x: durationData.map(item => item.x),
        y: durationData.map(item => item.y),
        type: 'bar',
        color: '#7FFF00'
    }];

    let keysPlotData = [{
        x: keysData.map(item => item.x),
        y: keysData.map(item => item.y),
        type: 'bar',
        color: '#00FA9A'
    }];

    self.postMessage({
        type: 'plot',
        durationPlotData: durationPlotData,
        keysPlotData: keysPlotData
    });
};
