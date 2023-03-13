# omr-scanner-api

## API Reference

#### Get Authentication Token

```http
  POST /api/auth/token
```
Form data:
| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `username` | `string` | **Required**. Your Username |
| `password` | `string` | **Required**. Your Password |   

Returns the api-key:
| Parameter | Value     | Description                |
| :-------- | :------- | :------------------------- |
| `token` | {api-key} | Your API Key(String) |

#### Upload Answer Sheet

```http
  POST /api/upload
```
Form data:
| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `sheet`      | `Image File` | **Required**. Answer Sheet |

Returns the status:
| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `status`      | `success` |Answer Sheet evaluated succesfully and data stored in db |
| `status`      | `failed` |Answer Sheet evaluated failed |
| `status`      | `error` |Error occured |
| `error`      | {error} |Only if status is `error`. Error Description(String)|
| `error_type`      | {error type} |Only if status is `error`. Error Type(String) |


#### For testing and demonstration purposes
```http
  GET /api/test
```
No authentication required
