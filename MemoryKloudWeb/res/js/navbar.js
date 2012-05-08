



function loadKloudletsList()

// Display a loading icon in our display element
//$('#mainTimeline').html('<span><img src="../img/ico-loading.gif" /></span>');
{            // Create an empty array to store kloudlets 
            kloudlets = [];
            var kloudletsID = [];
    // Request the JSON and process it
    $.ajax({
        type: 'GET',
        url: "http://beta.memorykloud.com:8080/json/kloudlet",
        data: "id=all",
        success: function (feed) {

            //sort feed by date
            feed.sort(sort_by('CREATED_ON', false));

            // Loop through the items
            for (var i = 0; i < feed.length; ++i) {
                // Find names of events and their IDs
                var event = feed[i].NAME;
                var eventID = feed[i].ID;
                // Add the new elements to two different  arrays
                kloudlets.push(event);
                kloudletsID.push(eventID);
            }
            //sort kloudlets in ascending order
            sort_by(kloudlets);

            // Display the events in a list with id elements on the page
            for (var i = 0; i < kloudlets.length; i++) {
                $('#navbar ul').append("<li> <a href='javascript:loadKloudlet(" + kloudletsID[i] + ")'>" + kloudlets[i] + "</a></li>");
            }

	    console.log(kloudlets);
            loadKloudlet(kloudletsID[0]);
            $('#kloudletTitle').html('').append(kloudlets[0]);
        },
        dataType: 'jsonp'

    });

}



//Load Kloudlet
function loadKloudlet(kloudletsID) {

    //Grab Event Title from navbar and append it to the top of #mainTimeline + flush all html in the #mainTimeline
    $('#navbar ul li a').click(function (e) {
        var txt = $(e.target).text();
        $('#mainTimeline').html('').append('<div id="kloudletTitleContainer"><div id="kloudletTitle">' + txt + '</div></div>');

    });


    // Request the JSON and process it
    $.ajax({
        type: 'GET',
        url: "http://beta.memorykloud.com:8080/json/moment2",
        data: "kid=" + kloudletsID,
        success: function (feed) {

            //sort feed by date
            feed.sort(sort_by('CREATED_ON', false));

            // Loop through the items
            var blobDataArray = [];
            var createdByArray = [];
            var createdOnArray = [];
            var geoLocationArray = [];
            var momentIDArray = [];
            var mediaIDArray = [];
            var parentIDArray = [];
            var mediaDescArray = [];
            var mediaTypeArray = [];
            var URLArray = [];
            //console.log(feed);
            //FAKE AVATARS
            var avatar = ["http://fbcdn-profile-a.akamaihd.net/hprofile-ak-snc4/161804_501897750_1815739058_n.jpg", "https://fbcdn-sphotos-a.akamaihd.net/hphotos-ak-snc6/199158_6201760351_530835351_33862_8019_n.jpg", "https://fbcdn-profile-a.akamaihd.net/hprofile-ak-snc4/48898_624505598_539_n.jpg", "https://fbcdn-profile-a.akamaihd.net/hprofile-ak-ash2/211764_644864940_1065975256_n.jpg", "https://fbcdn-profile-a.akamaihd.net/hprofile-ak-snc4/371020_615190773_598888761_n.jpg", "https://fbcdn-profile-a.akamaihd.net/hprofile-ak-ash2/211819_4001127_1650822609_n.jpg", "https://fbcdn-profile-a.akamaihd.net/hprofile-ak-ash2/573933_4302835_967332732_n.jpg"]



            for (var i = 0; i < feed.length; ++i) {
                // Find names of events and their IDs
                var blobData = feed[i].BLOBDATA;
                var createdBy = feed[i].CREATED_BY;
                var createdOn = feed[i].CREATED_ON;
                var geoLocation = feed[i].GEOLOCATION;
                var momentID = feed[i].ID;
                var mediaID = feed[i].MEDIA_ID;
                var parentID = feed[i].PARENTID;
                var mediaDesc = feed[i].TEXT;
                var mediaType = feed[i].TYPE;
                var URL = feed[i].URL;

                blobDataArray.push(blobData);
                createdByArray.push(createdBy);
                createdOnArray.push(createdOn);
                geoLocationArray.push(geoLocation);
                momentIDArray.push(momentID);
                mediaIDArray.push(mediaID);
                parentIDArray.push(parentIDArray);
                mediaDescArray.push(mediaDesc);
                mediaTypeArray.push(mediaType);
                URLArray.push(URL);



            }



            // Display the events in a list with id elements on the page
            for (var i = 0; i < feed.length; i++) {
                $('#mainTimeline').append('<div class="momentContainer"><img class="Avatar" src="http://fbcdn-profile-a.akamaihd.net/hprofile-ak-snc4/161804_501897750_1815739058_n.jpg"alt="" /><div class="objectContainer"><div class="KloudletUnitActor"><a href="http://www.memorykloud.com/user/' + createdByArray[i] + '">' + createdByArray[i] + ' uploaded an image.</a><span>' + createdOnArray[i] + '</span><div class="KloudletSelectorButton"></div></div><div class="photoWrap"><img src="http://beta.memorykloud.com:8080/file?url=' + blobDataArray[i] + '"alt="" /></div><h2><span>' + mediaDescArray[i] + '</span></h2></div></div>');



            }


        },
        dataType: 'jsonp'
    });

}

//Function to sort DESC
var sort_by = function (field, reverse) {
        reverse = (reverse) ? -1 : 1;
        return function (a, b) {
            a = a[field];
            b = b[field];
            if (a > b) return reverse * -1;
            if (a < b) return reverse * 1;
            return 0;
        }
    }

    //Function to initiate other functions
function addLoadEvent(func) {
    var oldonload = window.onload;
    if (typeof window.onload != 'function') {
        window.onload = func;
    } else {
        window.onload = function () {
            oldonload();
            func();
        }
    }
}


addLoadEvent(loadKloudletsList);
