function VideoPersisterXBlock(runtime, element) {

    var handlerUrl = runtime.handlerUrl(element, "studio_submit")

    $(element).find(".save-button").bind("click", function() {

		var formData = new FormData()
		var file_data = $(element).find("input").prop("files")[0]
		formData.append("file", file_data)

		runtime.notify("save", {
            state: "start"
        });

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
                        });
                    });
                } else {
                    runtime.notify("save", {
                        state: "end"
                    });
                }
            }
        })

    })

    $(element).find(".cancel-button").bind("click", function() {
        runtime.notify("cancel", {});
    });

    function onResponse(result) {
    	/** TODO: Handle server response */
    }
}
