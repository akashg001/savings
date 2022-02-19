const Chartyear=(data,labels)=>{
    
    var ctx = document.getElementById('year_myChart').getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'pie',
        data: {
             labels: labels,
            datasets: [{
                label: 'Total expenses',
                 data: data,
                backgroundColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            title: {
                
                display : false,
                text : 'Expense per Category',
            }
        }
    });
    }
    
    const chartDatayear=()=>{
        console.log('fetching');
        fetch('/expense_category_year')
        .then(res=>res.json())
        .then(results=>{
            console.log('results',results);
            const category_data=results.expense_category_data;
            const[labels,data]=[Object.keys(category_data),Object.values(category_data)];
    
            Chartyear(data,labels);
        })
    };
    
    document.onload=chartDatayear()
    