The application directory is a new root directory withing the collection structure. It will contain subdirectories, one for each auotmation application.

The directory should reflect the name of the automation application but should not be used to derive information about the automation application.

Files:

- `description.xx-yy.yaml`: - Information related to the descirption of the automation application. - xx if the ISO 639 lanugage code - yy is the ISO 3166 country code
- `input.json`: - The input data for the automation application formatted as a json schema (2020-12).
- `output.json`: - The output data for the automation application formatted as a json schema (2020-12).

Notes:

- The version of the automation application will be the same as the version of the collection
- json schema keys should follow python naming conventions
