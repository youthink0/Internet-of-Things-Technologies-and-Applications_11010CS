var date = "";
// Given a date in above format, return
// previous day as a date object
function getYesterday(d) 
{
    d = stringToDate(d);
    d.setDate(d.getDate() - 1)
    return d;
}

function print_date_message()
{
    // `date` is a `Date` object
    const formatYmd = date => date.toISOString().slice(0, 10);
    var now = new Date();
    var day_diff = 1000 * 60 * 60 * 24 * 1;
    
    var e = document.getElementById("dates").value;
     
    //window.alert(date_var);
    var date = "";
    if (e=="today")
    {
        document.getElementById( 
                    "message").innerHTML = "顯示日期 : " + String(formatYmd(now)); 
        date = String(formatYmd(now));    
    }
    else if (e=="yesterday")
    {
        var d = new Date(now - day_diff);
        document.getElementById( 
                    "message").innerHTML = "顯示日期 : " + String(formatYmd(d));
        date = String(formatYmd(d));    
    }     
    else if (e=="3days")
    {
        var d = new Date(now - day_diff*2);
        document.getElementById( 
                    "message").innerHTML = "顯示日期 : " + String(formatYmd(d));
        date = String(formatYmd(d));     
    } 
    else if (e=="4days")
    {
        var d = new Date(now - day_diff*3);
        document.getElementById( 
                    "message").innerHTML = "顯示日期 : " + String(formatYmd(d));
        date = String(formatYmd(d));
    } 
    else if (e=="5days")
    {
        var d = new Date(now - day_diff*4);
        document.getElementById( 
                    "message").innerHTML = "顯示日期 : " + String(formatYmd(d));
        date = String(formatYmd(d));
    }
    else if (e=="6days")
    {
        var d = new Date(now - day_diff*5);
        document.getElementById( 
                    "message").innerHTML = "顯示日期 : " + String(formatYmd(d));
        date = String(formatYmd(d));
    }
    else
    {
        var d = new Date(now - day_diff*12);
        document.getElementById( 
                    "message").innerHTML = "顯示日期 : " + String(formatYmd(d));
        date = String(formatYmd(d));
    }


    document.getElementById('imageBox').src = "picture/" + date + "_Line chart" + ".jpg"; 
    document.getElementById('imageBox1').src = "picture/" + date + " supply_use ratio" + ".jpg";
    document.getElementById('imageBox2').src = "picture/" + date + " time_use ratio" + ".jpg";       
}

function initialize()
{
    document.getElementById( 
                    "message").innerHTML = "顯示日期 : 無";
    date = "";
    document.getElementById('imageBox').src = "";
    document.getElementById('imageBox1').src = "";
    document.getElementById('imageBox2').src = "";
}

window.onload = function()
{ 
    
    print_date_message();
    initialize();
    var name = "kk";
    var lengthOfName = name.length;
    //document.getElementById('message').innerHTML = name;  
  
};
