"""HTTP client module for making requests to the Rubrik API."""

import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional, Union
from urllib.parse import urljoin

import requests
import urllib3
from requests.exceptions import RequestException

from configuration.configuration import load_config
from exceptions import RubrikAPIError, ConfigurationError

# Suppress insecure request warnings - TODO: Make this configurable
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logger = logging.getLogger(__name__)

class RubrikClient:
    """Client for making HTTP requests to the Rubrik API."""

    def __init__(self) -> None:
        """Initialize the Rubrik client with configuration."""
        try:
            config = load_config()
            json_config_path = Path(config["root_dir"]) / "configuration" / "config.json"
            
            # Load raw config values from JSON
            with open(json_config_path, "r") as f:
                self.config = json.load(f)
                
            self.base_url = self.config["graphql_url"]
            self.token_url = self.config["access_token_uri"]
            self._access_token: Optional[str] = None
            logger.debug("RubrikClient initialized successfully")
        except Exception as e:
            error_msg = "Failed to initialize RubrikClient"
            logger.exception(error_msg)
            raise ConfigurationError(f"{error_msg}: {str(e)}") from e

    @property
    def access_token(self) -> Optional[str]:
        """Get the current access token."""
        return self._access_token

    def authenticate(self) -> Optional[str]:
        """
        Authenticate with the Rubrik API using client credentials.

        Returns:
            Optional[str]: The access token, or None if authentication fails

        Raises:
            RubrikAPIError: If authentication fails
        """
        try:
            headers = {'Content-Type': 'application/json'}
            data = {
                'client_id': self.config["client_id"],
                'client_secret': self.config["client_secret"]
            }

            response = requests.post(
                self.token_url,
                data=json.dumps(data),
                headers=headers,
                verify=False  # TODO: Make this configurable
            )

            if response.status_code != 200:
                raise RubrikAPIError(
                    f"Authentication failed with status {response.status_code}: {response.text}"
                )

            self._access_token = response.json()["access_token"]
            logger.info("Successfully authenticated with Rubrik API")
            return self._access_token

        except RequestException as e:
            error_msg = "Failed to authenticate with Rubrik API"
            logger.exception(error_msg)
            raise RubrikAPIError(f"{error_msg}: {str(e)}") from e

    def logout(self) -> None:
        """
        Invalidate the current access token.

        Raises:
            RubrikAPIError: If logout fails
        """
        if not self._access_token:
            logger.warning("No active session to logout from")
            return

        try:
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self._access_token}'
            }

            # For Rubrik API, just clear the token without making a request
            self._access_token = None
            logger.info("Successfully cleared session token")

            self._access_token = None
            logger.info("Successfully logged out from Rubrik API")

        except RequestException as e:
            error_msg = "Failed to logout from Rubrik API"
            logger.exception(error_msg)
            raise RubrikAPIError(f"{error_msg}: {str(e)}") from e

    def graphql_request(
        self,
        query: str,
        variables: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Make a GraphQL request to the Rubrik API.

        Args:
            query: The GraphQL query string
            variables: Optional variables for the GraphQL query

        Returns:
            The JSON response from the API

        Raises:
            RubrikAPIError: If the request fails
            ValueError: If no access token is available
        """
        if not self._access_token:
            raise ValueError("No access token available. Call authenticate() first")

        try:
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self._access_token}'
            }

            payload = {'query': query}
            if variables:
                payload['variables'] = variables # type: ignore

            response = requests.post(
                self.base_url,
                json=payload,
                headers=headers,
                verify=False  # TODO: Make this configurable
            )

            if response.status_code != 200:
                raise RubrikAPIError(
                    f"GraphQL request failed with status {response.status_code}: {response.text}"
                )

            result = response.json()
            if 'errors' in result:
                raise RubrikAPIError(f"GraphQL errors: {json.dumps(result['errors'])}")

            return result

        except RequestException as e:
            error_msg = "Failed to execute GraphQL request"
            logger.exception(error_msg)
            raise RubrikAPIError(f"{error_msg}: {str(e)}") from e