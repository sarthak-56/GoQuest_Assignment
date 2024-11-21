from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .utils import fetch_channel_data, save_to_excel
from datetime import datetime
import os

class FetchYouTubeDataView(APIView):
    def post(self, request):
        channel_url = request.data.get("channel_url")
        if not channel_url:
            return Response({"error": "Channel URL is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Fetch video and comment data
            videos, comments = fetch_channel_data(channel_url)

            # Generate the output file name and save it to the desktop
            output_file_name = f"youtube_data_{datetime.now().strftime('%Y%m%d%H%M%S')}.xlsx"
            desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
            output_file_path = os.path.join(desktop_path, output_file_name)

            # Save data to an Excel file
            save_to_excel(videos, comments, output_file_path)

            # Return the data as JSON along with the file path
            return Response(
                {
                    "message": "Data fetched successfully",
                    "file_path": output_file_path,
                    "data": {
                        "videos": videos,
                        "comments": comments,
                    }
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
