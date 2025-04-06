# Riot Take-Home Technical Challenge

## Implementation notes

### Usage

A makefile allows for a quick and easy build, test and run.
Docker is mandatory to run it (and not install anything else on your machine).
The resulting image is about 120MB

### Implementation details

1. Contrarily to the given examples for the encrypt method, I have chosen to cast as json all values below the first level of nesting.
This allows to easily differentiate the values `123` and `"123"` which are two different json entries and should be decoded as such.
(The tests contain those entries).

This means that the payload `"John Doe"` has an encrypted value of `IkpvaG4gRG9lIg==` instead of `Sm9obiBEb2U=` because of the quotes.

2. Also, I have considered that a json payload consisting of an array at the root level is to be considered as a set of depth 1 properties.

3. For the API, I have considered that the expected design for the `/verify` endpoint should be followed for simplicity for all bad requests.
This means that all wrong queries to other endpoint will also handle errors with a `400 BAD REQUEST`.

4. Finally, the signing method has a default hmac algorithm of sha256 but it is configurable within the settings (in `/app/core/config.py`) and through env variables (by passing an env variable to the docker run command like `-e HMAC_DIGEST=md5`).
The signing key is generated in the config at the start of the container and could be loaded as a base64 encoded.


### Going beyond

Here are a few things I could have spend time doing but it was already quite some investment.

1. I didn't go to the extend of entirely managing logs in json, which is much nicer when using external tools to gather them
2. I didn't extend the API and middleware to manage all kind of errors and I let FastAPI do its basic handling of errors (other than the ones specifically handled).
3. I could have fuzzed the endpoints but I am not familiar with tools to do it and for this exercise the tests are already covering the major concerns.

## Overview

This challenge requires you to build an HTTP API with 4 endpoints that handle JSON payloads for encryption, decryption, signing, and verification operations.

## Requirements

### 1. Encryption Endpoint (`/encrypt`)

- **Method**: POST
- **Input**: Any JSON payload
- **Output**: JSON payload with all properties at depth 1 encrypted
- **Encryption Algorithm**: Base64 (for simplicity)

**Example**:

Input:

```json
{
  "name": "John Doe",
  "age": 30,
  "contact": {
    "email": "john@example.com",
    "phone": "123-456-7890"
  }
}
```

Output:

```json
{
  "name": "Sm9obiBEb2U=",
  "age": "MzA=",
  "contact": "eyJlbWFpbCI6ImpvaG5AZXhhbXBsZS5j..."
}
```

### 2. Decryption Endpoint (`/decrypt`)

- **Method**: POST
- **Input**: Any JSON payload
- **Output**: Original JSON payload with decrypted values. If some properties contain values which were not encrypted, they must remain unchanged.
- **Decryption Algorithm**: Base64 (for simplicity)

**Examples**:

Using the output from the `/encrypt` example as input should return the original payload:

Input:

```json
{
  "name": "Sm9obiBEb2U=",
  "age": "MzA=",
  "contact": "eyJlbWFpbCI6ImpvaG5AZXhhbXBsZS5j..."
}
```

Output:

```json
{
  "name": "John Doe",
  "age": 30,
  "contact": {
    "email": "john@example.com",
    "phone": "123-456-7890"
  }
}
```

Unencrypted properties must remain unchanged:

Input:

```json
{
  "name": "Sm9obiBEb2U=",
  "age": "MzA=",
  "contact": "eyJlbWFpbCI6ImpvaG5AZXhhbXBsZS5j...",
  "birth_date": "1998-11-19"
}
```

Output:

```json
{
  "name": "John Doe",
  "age": 30,
  "contact": {
    "email": "john@example.com",
    "phone": "123-456-7890"
  },
  "birth_date": "1998-11-19"
}
```

### 3. Signing Endpoint (`/sign`)

- **Method**: POST
- **Input**: Any JSON payload
- **Output**: JSON payload with a unique "signature" property
- **Signature Algorithm**: HMAC
- **Important Note**: The signature must be computed based on the value of the JSON payload, not its string representation. This means the order of properties should not affect the signature.

**Examples**:

Basic example for an object with two properties:

Input:

```json
{
  "message": "Hello World",
  "timestamp": 1616161616
}
```

Output:

```json
{
  "signature": "a1b2c3d4e5f6g7h8i9j0..."
}
```

The order of properties must not change the signature, which means this example will generate the same signature:

Input:

```json
{
  "timestamp": 1616161616,
  "message": "Hello World"
}
```

Output:

```json
{
  "signature": "a1b2c3d4e5f6g7h8i9j0..."
}
```

### 4. Verification Endpoint (`/verify`)

- **Method**: POST
- **Input**: JSON payload with "signature" and "data" properties
- **Output**:
  - HTTP 204 (No Content) if signature is valid
  - HTTP 400 (Bad Request) if signature is invalid

**Examples**:

Basic example of an object with two properties:

Input:

```json
{
  "signature": "a1b2c3d4e5f6g7h8i9j0...",
  "data": {
    "message": "Hello World",
    "timestamp": 1616161616
  }
}
```

Output: 204 HTTP response

The same input object with the order of properties changed must produce the same signature:

Input:

```json
{
  "signature": "a1b2c3d4e5f6g7h8i9j0...",
  "data": {
    "timestamp": 1616161616,
    "message": "Hello World"
  }
}
```

Output: 204 HTTP response

Example when using a tampered signature or payload:

Input:

```json
{
  "signature": "a1b2c3d4e5f6g7h8i9j0...",
  "data": {
    "timestamp": 1616161616,
    "message": "Goodbye World"
  }
}
```

Output: 400 HTTP response

## Design Considerations

1. **Abstraction**: The encryption algorithm (Base64) in the `/encrypt` and `/decrypt` endpoints should be easily replaceable with another algorithm without significant changes to the codebase. Design your solution with appropriate abstractions. The same principle applies to the signature algorithm used in the `/sign` and `/verify` endpoints.

2. **Consistency**: Ensure that `/encrypt` followed by `/decrypt` returns the original payload. Ensure that a payload signed with `/sign` can be successfully verified with `/verify`.

## Submission

Please submit your completed project by sending your GitHub repository link to louis@tryriot.com.
