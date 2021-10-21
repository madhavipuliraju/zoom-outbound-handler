import requests
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def generate_auth_token():
    """
    Generates the auth token
    """
    url = "https://zoom.us/oauth/token?grant_type=client_credentials"

    headers = {
        'Authorization': 'Basic cnlSX0tjVDZScWVKQzBhRDBEYVRZdzpNWFJlaXdvRThiRzhEalhEeDZqSzRja1k4VXo5YUh1VQ=='
    }

    response = requests.request("POST", url, headers=headers)
    if response.status_code == 200:
        return "Bearer " + response.json().get("access_token")

def send_message_to_zoom(creds, robot_jid, account_id, to_jid, message, is_agent, agent_name):
    """
    Sends message to zoom user
    """
    auth_token = generate_auth_token()
    send_message_url = "https://api.zoom.us/v2/im/chat/messages"
    data = {
        "robot_jid": robot_jid,
        "to_jid": to_jid,
        "account_id": account_id,
        "content": {
            "head": {
                "text": message
            }
        }
    }
    # if link:
        # data = {
        #   "robot_jid": "v1cut2lkpprq6bxkppdcfysa@xmpp.zoom.us",
        #   "to_jid": "v6wwmkykr7g8buzhftxmgw@xmpp.zoom.us",
        #   "account_id": "kca-jl8TSA63lXwnPqoplQ",
        #   "content": {
        #     "head": {
        #       "text": message
        #     },
        #     "body": [
        #     {
        #       "type": "message",
        #       "text": "Visit Link 🔗",
        #       "link": link
        #     }
        #   ]
        #   }
        # }
    headers = {"Authorization": auth_token, "Content-Type": "application/json"}
    logger.info(f"Trying to send a message to Zoom: {message}")
    
    if is_agent:
        data["username"] = agent_name
        data["icon_emoji"] = ":computer:"
    try:
        logger.info(
            f"Sending message to zoom with payload:\n{data} and headers:\n{headers}")
        response = requests.request("POST", send_message_url, headers=headers, json=data)
        logger.debug(f"Response of send message to zoom:\n{response.text}")
        logger.info(f"Response Status Code of send message to zoom:\n{response.status_code}")
        logger.info(f"Payload of send message to zoom:\n{data}")
        if response.status_code == 201:
            return response
        else:
            raise Exception(
                f"[UNEXPECTED STATUS CODE: {response.status_code}]")
    except Exception as ex:
        logger.error(
            f"Encountered exception while sending message to zoom:\n{ex}")

def send_message_with_button_to_zoom(link_list, is_link, is_text, item_list, creds, robot_jid, account_id, to_jid, message, is_agent, agent_name):
    """
    Sends message with button to zoom user
    """
    auth_token = generate_auth_token()
    send_message_url = "https://api.zoom.us/v2/im/chat/messages"
    if is_link and is_text:
        logger.info("The button is for Is_link and is_text")
        link_list.append({
                         "type":"actions",
                         "items":item_list
                      })
        data = {
           "robot_jid":robot_jid,
           "to_jid":to_jid,
           "account_id":account_id,
           "content":{
              "head":{
                 "text":message
              },
              "body": link_list
           }
        }
    elif is_link:
        logger.info("The button is for Is_link")
        data = {
          "robot_jid": robot_jid,
          "to_jid": to_jid,
          "account_id": account_id,
          "content": {
            "head": {
              "text": message
            },
            "body": link_list
          }
        }
    elif is_text:
        logger.info("The button is for is_text")
        data = {
           "robot_jid":robot_jid,
           "to_jid":to_jid,
           "account_id":account_id,
           "content":{
              "head":{
                 "text":message
              },
              "body":[
              {
                 "type":"actions",
                 "items":item_list
              }
           ]
           }
        }
    
    headers = {"Authorization": auth_token, "Content-Type": "application/json"}
    logger.info(f"Trying to send a message with buttons to Zoom: {message}")
    logger.info(f"Send a message with buttons to Zoom Payload: {data}")
    try:
        response = requests.request(
            "POST", send_message_url, headers=headers, json=data
        )
        logger.info(f"Send Button to Zoom Response status: {response.status_code}")
        logger.info(f"Send Button to Zoom Payload: {data}")
        if response.status_code == 201:
            return response.json().get("id")
    except Exception as ex:
        logger.error(f"Exception raised while sending the message to the conversation: {ex}")

# def send_block_message_to_zoom(item_list, creds, channel, message, is_agent, agent_name):
#     """
#     Sends message to zoom user
#     """
#     url = "https://zoom.com/api/chat.postMessage"
#     headers = {
#         'Content-Type': "application/json",
#         'Authorization': creds["zoom_auth"]
#     }
    
#     data = {
#         "channel":channel,
#         "text": message,
#         "blocks":[
#             {
#                 "type":"actions",
#                 "block_id":"actionblock789",
#                 "elements": item_list
#             }
#         ]
#     }
    
#     if is_agent:
#         data["username"] = agent_name
#         data["icon_emoji"] = ":computer:"
#     try:
#         logger.info(
#             f"Sending block message to zoom with payload:\n{data} and headers:\n{headers}")
#         response = requests.request("POST", url, headers=headers, json=data)
#         logger.debug(f"Response of send block message to zoom:\n{response.text}")
#         logger.info(f"Response Status Code of send block message to zoom:\n{response.status_code}")
#         logger.info(f"Payload of send block message to zoom:\n{data}")
#         if response.status_code == 200:
#             return response
#         else:
#             raise Exception(
#                 f"[UNEXPECTED STATUS CODE: {response.status_code}]")
#     except Exception as ex:
#         logger.error(
#             f"Encountered exception while sending block message to zoom:\n{ex}")


# def send_file_to_zoom(creds, channel, text, thumb_url, is_agent, agent_name):
#     """
#     Sends the Attachment to zoom
#     """
#     url = "https://zoom.com/api/chat.postMessage"
#     attachments = [{"text": text, "id": 1, "fallback": "",
#                     "image_url": thumb_url, "thumb_url": thumb_url}]
#     headers = {
#         "Content-Type": "application/json",
#         "Authorization": creds["zoom_auth"]
#     }
#     data = {
#         "channel": channel,
#         "attachments": json.dumps(attachments)
#     }
#     if is_agent:
#         data["username"] = agent_name
#         data["icon_emoji"] = ":computer:"
#     try:
#         logger.info(
#             f"Sending file to zoom with payload:\n{data} and headers:\n{headers}")
#         zoom_response = requests.post(
#             url, data=json.dumps(data), headers=headers)
#         logger.debug(
#             f"Response of send message to zoom:\n{zoom_response.text}")
#         if zoom_response.status_code == 200:
#             return zoom_response
#         else:
#             raise Exception(
#                 f"[UNEXPECTED STATUS CODE: {zoom_response.status_code}]")
#     except Exception as ex:
#         logger.error(
#             f"Encountered exception while sending message to zoom:\n{ex}")
