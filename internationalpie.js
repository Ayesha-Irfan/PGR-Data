var stipend = 1472;
var housing = 977;
var bills = 118;
var food = 194

var remaining = stipend - housing - bills;

// creates a pie chart showing this data

var data = [
    {
        values: [housing, bills, food, remaining],
        labels: ['Housing', 'Bills', 'Food', 'Remaining'],
        type: 'pie',
        textinfo: "label+percent",
        textposition: "outside",
    }];

var layout = {
    paper_bgcolor: 'rgba(0,0,0,0)',
    plot_bgcolor: 'rgba(0,0,0,0)',
    height: 400,
    width: 500,
    showlegend: false,
    title: 'Monthly Costs Breakdown',
    font: {
        family: 'Arial',
        size: 16,
        color: '#ffffff'

    },
    
};

var config = {
    responsive: true,
    displayModeBar: false,

};

Plotly.newPlot('internationalpie', data, layout, config);