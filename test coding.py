from pathlib import Path

from autogen_core import CancellationToken
from autogen_core.code_executor import CodeBlock
from autogen_ext.code_executors.local import LocalCommandLineCodeExecutor

work_dir = Path("coding")
work_dir.mkdir(exist_ok=True)


#first save the code to file in dir, and then run the file with command line
async def execute_code():
    local_executor = LocalCommandLineCodeExecutor(work_dir=work_dir)
    result = await local_executor.execute_code_blocks(
        code_blocks=[
            CodeBlock(language="python", code="print('Hello, World!')"),
        ],
        cancellation_token=CancellationToken(),
    )
    print(result)

# Call the async function
import asyncio
asyncio.run(execute_code())