# SMB2 Client for Node.js

[![Node compatibility](https://badgen.net/npm/node/pv-node-smb2)](https://npmjs.org/package/pv-node-smb2) [![License](https://badgen.net/npm/license/pv-node-smb2)](https://npmjs.org/package/pv-node-smb2) [![PackagePhobia](https://badgen.net/packagephobia/install/pv-node-smb2)](https://packagephobia.now.sh/result?p=pv-node-smb2)

[![Package Version](https://badgen.net/npm/v/pv-node-smb2)](https://npmjs.org/package/pv-node-smb2) [![Latest Commit](https://badgen.net/github/last-commit/Node-SMB/marsaud-smb2)](https://github.com/Node-SMB/marsaud-smb2/commits/master)

## Introduction

This library calls the C libraries for libsmbclient to read and search through directories.

The original fork was unable to connect to newer servers, and rather than hacking about with the smb2 protocol, it is far easier to 
leverage the great work of the samba team, and use their libsmbclient library via NAPI bindings.
This is much quicker than other wrappers that fork/exec smbclient, and the only OS pre-req is to install the libsmbclient library.

## Prerequisites

### macOS
Install samba via Homebrew:
```bash
brew install samba
```

### Linux
Install the libsmbclient development package:
```bash
sudo apt-get install libsmbclient-dev  # Debian/Ubuntu
# or
sudo yum install libsmbclient-devel     # RHEL/CentOS
```

## Installation

```bash
npm install -S pv-node-smb2
```

## API

### Asynchronicity

No async calls supported yet; there's a skeleton for a read function, but much more work is still needed.


### Sync calls

#### Reading Files

```typescript
import {PvDirent,PvNodeSmb2} from 'pv-node-smb2'

const smb2Client = new PvNodeSmb2('workgroup', 'user', 'password')

// Read a file from SMB share
const content = smb2Client.readFileSync('smb://<host or IP>/Windows Path/goes/here/foo.txt')
console.log(content.toString('base64'))
// or
console.log(content.toString('utf8'))
```

#### Getting File Information

```typescript
// Get file metadata
const fileInfo: PvDirent = smb2Client.fileInfo('smb://<host or IP>/Windows Path/goes/here/foo.txt')
console.log(`File: ${fileInfo.name}`)
console.log(`Size: ${fileInfo.size} bytes`)
console.log(`Is File: ${fileInfo.isFile}`)
console.log(`Is Directory: ${fileInfo.isDir}`)
console.log(`Modified: ${fileInfo.mtime}`)
console.log(`Created: ${fileInfo.btime}`)
```

#### Reading Directories

```typescript
// Read directory contents
const entries: PvDirent[] = smb2Client.readDir('smb://<host or IP>/Windows Path/goes/here/')
entries.forEach(entry => {
  console.log(`${entry.isDir ? '[DIR]' : '[FILE]'} ${entry.name} (${entry.size} bytes)`)
})
```

#### Writing Files

```typescript
// Write a buffer to SMB share (overwrites if file exists)
const dataBuffer = Buffer.from("Hello, World!", "utf8")
const bytesWritten = smb2Client.writeFileSync('smb://<host or IP>/Windows Path/goes/here/foo.txt', dataBuffer)
console.log(`Written ${bytesWritten} bytes`)
```

#### Renaming/Moving Files

```typescript
// Rename or move a file on SMB share
const result = smb2Client.renameFileSync(
  'smb://<host or IP>/Windows Path/goes/here/foo.txt',
  'smb://<host or IP>/Windows Path/goes/here/bar.txt'
)
// Returns 0 if successful
```

#### Deleting Files

```typescript
// Delete a file from SMB share
const result = smb2Client.unlinkFileSync('smb://<host or IP>/Windows Path/goes/here/foo.txt')
// or use the alias
const result2 = smb2Client.deleteFileSync('smb://<host or IP>/Windows Path/goes/here/bar.txt')
// Returns 0 if successful
```

#### Complete Example

```typescript
import {PvDirent, PvNodeSmb2} from 'pv-node-smb2'

const smb2Client = new PvNodeSmb2('workgroup', 'user', 'password')

try {
  // Read a file
  const content = smb2Client.readFileSync('smb://server/share/file.txt')
  console.log(content.toString('utf8'))
  
  // Get file info
  const info = smb2Client.fileInfo('smb://server/share/file.txt')
  console.log(`File size: ${info.size} bytes`)
  
  // List directory
  const entries = smb2Client.readDir('smb://server/share/')
  entries.forEach(entry => {
    console.log(entry.name)
  })
  
  // Write a file
  const data = Buffer.from('Hello from Node.js!', 'utf8')
  smb2Client.writeFileSync('smb://server/share/newfile.txt', data)
  
  // Rename a file
  smb2Client.renameFileSync(
    'smb://server/share/newfile.txt',
    'smb://server/share/renamed.txt'
  )
  
  // Delete a file
  smb2Client.unlinkFileSync('smb://server/share/renamed.txt')
  
} catch (error) {
  console.error('SMB operation failed:', error)
} finally {
  // Clean up connection
  smb2Client.deleteContext()
}
```


### Connection management

Each instance of the PvNodeSmb2 class will have its own connection.


## Contributors

- [Leo Martins](https://github.com/pontusvision)
- [Marek](https://github.com/paulsoning)

## References

    The[MS-SMB2]: Server Message Block (SMB) Protocol Versions 2 and 3
    Copyright (C) 2014 Microsoft
    http://msdn.microsoft.com/en-us/library/cc246482.aspx

## License

(The MIT License)

Copyright (c) 2013-2014 Benjamin Chelli &lt;benjamin@chelli.net&gt;

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
'Software'), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
