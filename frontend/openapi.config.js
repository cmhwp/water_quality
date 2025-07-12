import { generateService } from '@umijs/openapi'

export default generateService({
  requestLibPath: 'import request from "@/utils/request"',
  schemaPath: 'http://localhost:8000/api/v1/openapi.json',
  serversPath: './src/services',
}) 