/*
 * Filename:     JQScripts.js
 * Author:       Andrew Laing
 * Email:        parisianconnections@gmail.com
 * Last updated: 19/08/2019.
 * Description:  JQuery scripts used by the 'Today I Have ...' website.
 */

$(document).ready(function(){
    /**
     * Opens the loginModal
     */
    $("#loginBtn").click(function(){
        $("#loginModal").modal();
    });


    /**
     * Displays a dropdown's links when the user hovers over it.
     */ 
    $(".dropdown").hover(
        function () { $(this).addClass('open') },
        function () { $(this).removeClass('open') }
    );


    /**
     * Opens the deleteAccountModal
     */
    $("#deleteAccountBtn").click(function(){
        $("#deleteAccountModal").modal();
    });


    /**
     * Clears the fields of the deleteAccountModal when it is closed.
     */
    $('#deleteAccountModal').on('hidden.bs.modal', function () {
        $('#frmDeleteAccount')[0].reset();
    });


    $.delete_user_account = function (data) {
        // post to account deleted here with reasons no password
        //document.location.href =  "/accountdeleted/";
        var csrftoken = getCookie('csrftoken');
        var p_reason = $(reasonsList).val();

        $.redirect("/accountdeleted/", {
            'reason': p_reason,
            'csrfmiddlewaretoken': csrftoken });
    };

    $.confirm_deleteAccount = function (data) {
        if (data === 'True') {
            if (confirm("Are you sure you want to delete your account?")) {
                alert("You're account will now be deleted!");
                $("#deleteAccountModal").modal('toggle');
                $.delete_user_account();
                return true;
            }
            else {
                alert("Operation cancelled.");
                $("#deleteAccountModal").modal('toggle');
                return false;
            }
        }
        else {
            alert('You have entered an incorrect password!');
            return false;
        }
    };


    /**
     * Checks that the user has filled in all fields 
     * in the addUpdateModal before submission.
     */
    $.entered_password_is_valid = function (p_password) {
        result = false;
        var csrftoken = getCookie('csrftoken');

        $.post("/checkuserpassword/",
            {
                pwd: p_password,
                csrfmiddlewaretoken: csrftoken
            },
            function (data, status) {
                //alert("Data: " + data + "\nStatus: " + status);
                if (status === 'success') {
                    if (data === 'True' || data === 'False') {
                        $.confirm_deleteAccount(data);
                    } else {
                        alert("Error: Cannot perform this action. please contact the administrator.");
                        $("#deleteAccountModal").modal('toggle');
                    }
                }
                else {
                    alert("Error: Cannot perform this action. please contact the administrator.");
                    $("#deleteAccountModal").modal('toggle');
                }
            });
    };


    /**
     * Checks that the user has filled in all fields 
     * in the addUpdateModal before submission.
     */
    $.validate_deleteAccount = function () {
        var password = $("#pwd_deleteModal").val()
        $.entered_password_is_valid(password);
    };


    /**
     * Stops the user from entering blocked characters into the
     * addUpdateModal's input fields to try and prevent XSS attacks.
     */
    $("#addUpdateModal input").on("keypress paste", function (e) {
        var c = this.selectionStart, v = $(this).val();
        if (e.type == "keypress")
            var key = String.fromCharCode(e.charCode ? e.charCode : e.which)
        else
            var key = e.originalEvent.clipboardData.getData('Text')

        var val = v.substr(0, c) + key + v.substr(c, v.length)

        var r_pattern = /[\<\>\&]+/

        if (val.match(r_pattern) || val.match(r_pattern).toString() == val) {
            e.preventDefault()
            alert('Sorry you cannot enter the <, > or & characters into this form!');
            return false
        }
    })


    /**
     * Stops the user from entering blocked characters into the
     * addUpdateModal's text area to try and prevent XSS attacks.
     */
    $("#addUpdateModal textarea").on("keypress paste", function (e) {
        var c = this.selectionStart, v = $(this).val();
        if (e.type == "keypress")
            var key = String.fromCharCode(e.charCode ? e.charCode : e.which)
        else
            var key = e.originalEvent.clipboardData.getData('Text')

        var val = v.substr(0, c) + key + v.substr(c, v.length)

        var r_pattern = /[\<\>\&]+/

        if (val.match(r_pattern) || val.match(r_pattern).toString() == val) {
            e.preventDefault()
            alert('Sorry you cannot enter the <, > or & characters into this form!');
            return false
        }
    })


    /**
     * Opens the addUpdateModal if the user has not posted today.
     */
    $("#addUpdateBtn").click(function () {
        $.ajax({
            url: "/haspostedtoday/",
            type: 'get',
            success: function (data) {
                if (data === 'True') {
                    // User has already posted today!
                    alert("Sorry. You have already posted today's update.");
                } else if (data!=='False') {
                    alert("Database error: please contact the administrator.");    
                } else {
                    // Show the add update modal 
                    $("#addUpdateModal").modal();
                }   
            },
            error: function () {
                alert('Error: please contact the site administrator.');
            }
        });
    }); 


    /**
     * Checks that the user has filled in all fields 
     * in the addUpdateModal before submission.
     */
    $.validate_addUpdate_fields = function() {
        var postTitleLen = $("#postTitle").val().length;  
        var postTextLen = $("#postText").val().length;  
        var postTagsLen = $("#tagDiv").val().length;  
        
        if(postTitleLen==0 || postTextLen==0 || postTagsLen==0 ) {
            alert("Please complete ALL of the data fields!");
            return false;
        }
        return true;
    };


    /**
     * Checks that the user has filled in both fields
     * in the LoginModal before submission.
     */
    // 
    $.validate_login = function() {
        var usernameLen = $("#username").val().length;  
        var passwordLen = $("#pwd").val().length;  
        
        if(usernameLen===0 || passwordLen===0) {
            alert("Error - both fields must be completed!");
            return false;
        }
        return true;
    };


    /**
     * Confirms that the user logout wishes to log out.
     */
    $.confirm_logout = function() {
        var r = confirm("Are you sure you want to log out of your account?");

        if (r == true) {
            alert("You are now logged out.");
        } else {
            return false;
        } 
    };


    /**
     * Returns the contents of a Cookie with the name specified,
     * or null if the Cookie name was not found.
     * Needed to get the CSRF token for POST requests.
     * Source: https://docs.djangoproject.com/en/2.2/ref/csrf/
     */
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }


    /**
     * Verifies that the user has chosen a unique title
     * for their post on the addUpdateModal when they leave the
     * postTitle field.
     */
    $("#postTitle").change(function() {
        var p_postTitle = $("#postTitle").val();
        var csrftoken = getCookie('csrftoken');

        $.post("/titleexists/",
        {
            title: p_postTitle,
            csrfmiddlewaretoken: csrftoken,
        },
        function(data, status) {
            if(status==='success') {
                if(data==='True') {
                    alert('Sorry. You must choose a unique title.');
                    $("#postTitle").val("");
                } else if (data!=='False') {
                    alert("Database error: please contact the administrator.");    
                    $("#addUpdateModal").modal('toggle');  // Hide the add update modal.
                }  
            }
            else {
                alert("Database error: please contact the administrator.");
                $("#addUpdateModal").modal('toggle');
            }
        });
    }); 


    /**
     * Handles the SUBMIT click for the addUpdateModal.
     */
    $('#frmAddUpdate').submit(function(e){
        e.preventDefault();
        var p_postTitle = $("#postTitle").val();
        var p_postText  = $("#postText").val();
        var p_postTags = $("#tagDiv").val();
        var csrftoken = getCookie('csrftoken');

        $.post("/addnewupdate/",
        {
            postTitle: p_postTitle,
            postText: p_postText,
            postTags: JSON.stringify(p_postTags),
            csrfmiddlewaretoken: csrftoken,
        },
        function(data, status) {
            if (status === 'success') {
                if(data==='True') {
                    alert('Your update has been added.');
                } else if (data!=='False') {
                    alert("Database error: please contact the administrator.");    
                } else {
                    alert('Sorry. Unable to add your update.');
                }    
            }
            else {
                alert("Database error: please contact the administrator.");
                $("#postTitle").val("");
            }
        });

        // Hide the add update modal.
        $("#addUpdateModal").modal('toggle');
    });


    /**
     * Clears the fields of the addUpdateModal when it is closed.
     */
    $('#addUpdateModal').on('hidden.bs.modal', function () {
        $('#frmAddUpdate')[0].reset();   
        $("#postTags").tagsinput('removeAll');       
    });


    /**
     * Changes the updates shown when a username link is clicked
     * on the MyUpdates and Tags pages.
     */
    function change_updates_by_username(posterName, csrftoken) {
        $.post("/src/ajaxhandlers/addUpdatesToPage.php",
        {
            username: posterName,
            csrfmiddlewaretoken: csrftoken,
        },
        function(data, status) {
            if(status==='success') {
                $("#userUpdates").empty().append(data);
                $("#tagList").empty().append(data);
            }
            else {
                alert("Sorry: Unable to retrieve your data.");
            }
        });
    };


    /**
     * Changes the updates shown when a username link is clicked
     * on the NewUpdates page.
     */
    $(".allUserUpdates").on("click",".panel-postTitle .posterName", function(e) {   
        e.preventDefault();       
        var posterName = $(this).attr("name");
        var csrftoken = getCookie('csrftoken');

        $.post("/addupdatesforusername/",
            {
                username: posterName,
                csrfmiddlewaretoken: csrftoken,
            },
            function (data, status) {
                if (status === 'success') {
                    $(".allUserUpdates").empty().append(data);
                }
                else {
                    alert("Sorry: Unable to retrieve your data.");
                }
            });
    }); 


    /**
     * Changes the updates shown when a username link is clicked
     * on the MyUpdates page.
     */
    $(".currentUserUpdates").on("click",".panel-postTitle .posterName", function(e) {   
        e.preventDefault();       
        var posterName = $(this).attr("name");
        var csrftoken = getCookie('csrftoken');

        $.post("/addupdatesforusername/",
            {
                username: posterName,
                csrfmiddlewaretoken: csrftoken,
            },
            function (data, status) {
                if (status === 'success') {
                    $(".currentUserUpdates").empty().append(data);
                }
                else {
                    alert("Sorry: Unable to retrieve your data.");
                }
            });
    }); 


    /**
     * Changes the updates shown when a tag link is clicked
     * on the myUpdates page.
     */
    $(".currentUserUpdates").on("click",".panel-footer .tagName", function(e) {   
        e.preventDefault();
        var tagName = $(this).attr("name");
        var showAllUserUpdates = "false";
        var csrftoken = getCookie('csrftoken');

        $.post("/addupdatesfortagbyloggedinuser/",
            {
                postTag: tagName,
                csrfmiddlewaretoken: csrftoken,
                showAll: showAllUserUpdates
            },
            function (data, status) {
                if (status === 'success') {
                    $(".currentUserUpdates").empty().append(data);
                }
                else {
                    alert("Sorry: Unable to retrieve your data.");
                }
            });
    }); 


    /**
     * Changes the div content to show updates when a tag link 
     * is clicked on the Tags or New Updates pages
     */
    $(".allUserUpdates").on("click",".panel-footer .tagName", function(e) {   
        e.preventDefault();       
        var tagName = $(this).attr("name");
        var showAllUserUpdates = "true";
        var csrftoken = getCookie('csrftoken');

        $.post("/addupdatesfortag/",
        {
            postTag: tagName,
            csrfmiddlewaretoken: csrftoken,
            showAll: showAllUserUpdates
        },
        function(data, status) {
            if(status==='success') {
                $(".allUserUpdates").empty().append(data);
            }
            else {
                alert("Sorry: Unable to retrieve your data.");
            }
        });
    }); 

});
