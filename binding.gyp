{
  "targets": [
    {
      "target_name": "pv",
      "sources": [ 
        "src/binding.c"
      ],
      "cflags!": [ "-fno-exceptions" ],
      "cflags_cc!": [ "-fno-exceptions" ],
      "conditions": [
        ["OS=='mac'", {
          "variables": {
            "homebrew_prefix%": "<!@(node -e \"const os = require('os'); const arch = os.arch(); console.log(arch === 'arm64' ? '/opt/homebrew' : '/usr/local');\")"
          },
          "include_dirs": [
            "<(homebrew_prefix)/include/samba-4.0",
            "<(homebrew_prefix)/include"
          ],
          "link_settings": {
            "libraries": [
              "-L<(homebrew_prefix)/lib",
              "-lsmbclient"
            ]
          },
          "xcode_settings": {
            "GCC_ENABLE_CPP_EXCEPTIONS": "YES",
            "CLANG_CXX_LIBRARY": "libc++",
            "MACOSX_DEPLOYMENT_TARGET": "10.7",
            "OTHER_LDFLAGS": [
              "-L<(homebrew_prefix)/lib"
            ]
          }
        }],
        ["OS=='linux'", {
          "include_dirs": [
            "/usr/include/samba-4.0",
            "/usr/include/node/"
          ],
          "libraries": [
            "/usr/lib/x86_64-linux-gnu/libsmbclient.so"
          ]
        }]
      ],
      "msvs_settings": {
        "VCCLCompilerTool": { "ExceptionHandling": 1 }
      }
    }
  ]
}
