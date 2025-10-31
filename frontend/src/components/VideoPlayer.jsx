import React from "react";

const VideoPlayer = ({ videoUrl }) => {
  return (
    <div className="w-full rounded-xl overflow-hidden shadow-lg bg-black">
      <video
        controls
        className="w-full aspect-video"
        src={videoUrl}
        controlsList="nodownload"
      />
    </div>
  );
};

export default VideoPlayer;
