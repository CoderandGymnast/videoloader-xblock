function VideoPersisterXBlock(runtime, element) {

    /**
    * ----------
    * PERSISTENCE:
    * ----------
    */

    const handlerUrl = runtime.handlerUrl(element, "studio_submit")

    $(element).find(".save-button").bind("click", function() {

        const formData = new FormData()
        const videoUrl = $("#video-url").val()
        const displayName = $("#display-name").val()
        
        formData.append("video_url", videoUrl)
        formData.append("display_name", displayName)

		runtime.notify("save", {
            state: "start"
        })

		$.ajax({
            url: handlerUrl,
            dataType: "json",
            cache: false,
            contentType: false,
            processData: false,
            data: formData,
            type: "POST",
            success: onResponse
        })
    })

    $(element).find(".cancel-button").bind("click", function() {
        runtime.notify("cancel", {})
    })

    function onResponse(response) {
        if (response.errors.length > 0) {
            response.errors.forEach(function(error) {
                runtime.notify("error", {
                    "message": error,
                    "title": "Scorm component save error"
                })
            })
        } else {
            runtime.notify("save", {
                state: "end"
            })
        }
    }

    /**
     * ----------
     * SELECTION:
     * ----------
     */

    /** TODO: Directly get data from Django server. */
    const wasUrlEmbedded = $("#was-url-embedded").text()
    if(wasUrlEmbedded === "False") $("#url-input").hide()    
    else $("select").val("youtube")

    $("select").on("change", function (e) {
        const HACHIUM_YOUTUBE_STUDIO = "https://studio.youtube.com/channel/"
        const selectedValue = this.value
        if(selectedValue === "youtube") {
            window.open(HACHIUM_YOUTUBE_STUDIO)
            $("#url-input").show()  
        } else {
            $("#video-url").val("")
            $("#url-input").hide()
        } 
   })   
}

/**
 * NOTE: The following code snippet is used to send file from browser cache to Django server.
 
        const formData = new FormData()
		const file_data = $(element).find("#uploaded_video").prop("files")[0]
        formData.append("file", file_data)

		runtime.notify("save", {
            state: "start"
        })

		$.ajax({
            url: handlerUrl,
            dataType: "json",
            cache: false,
            contentType: false,
            processData: false,
            data: formData,
            type: "POST",
            success: function(response) {
                if (response.errors.length > 0) {
                    response.errors.forEach(function(error) {
                        runtime.notify("error", {
                            "message": error,
                            "title": "Scorm component save error"
                        })
                    })
                } else {
                    runtime.notify("save", {
                        state: "end"
                    })
                }
            }
        })

 */

        