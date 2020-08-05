/** NOTE: Must define "VideoLoaderXBlock" to get rid of the error: "TypeError: Cannot read property 'prototype' of undefined". Because at server, this function name is used to initiate view.  */
function VideoLoaderXBlock(runtime, element) {

}

/**
 * NOTE: The following code snippet is used to load .m3u8 video of HACHIUM. 
 
 	videojs.Hls.xhr.beforeRequest = function (options) {
   	options.uri = options.uri + "?session_id=1"
       return options
   }

	$(document).ready(function(){
   	player195206 = videojs("play-video-195206")
       player195206.src({
       	src: "https://phamhieu.dev.hachium.com/streaming/6658b9fc85f4057438ff6ace48582306/1552373176099/720.m3u8",
           type: "application/vnd.apple.mpegurl"
       })
       player195206.width((window.innerHeight - 180) * 16 / 9)
       player195206.height(window.innerHeight - 180)
   })

*/
