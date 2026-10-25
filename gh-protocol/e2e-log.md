## gh-protocol E2E log — 2026-10-25T10:23:28Z

### pre-flight-diag.log (KVM/SDK)
== pre-flight 2026-10-25T10:21:53Z ==
runner: x86_64, nproc=4, mem=15G
kvm: crw-rw---- 1 root kvm 10, 232 Oct 25 10:14 /dev/kvm
ANDROID_HOME=/usr/local/lib/android/sdk
dl.google.com repo xml: HTTP 200
sdk pre-install OK: 4.2G system-images
kvm device present + sudo OK — emulator will run as root
pre-flight OK

### avd-create.log (tail)
total 16
drwxr-xr-x 3 runner runner 4096 Oct 25 10:22 .
drwxr-xr-x 3 runner runner 4096 Oct 25 10:22 ..
drwxr-xr-x 3 runner runner 4096 Oct 25 10:22 gh_test.avd
-rw-r--r-- 1 runner runner  115 Oct 25 10:22 gh_test.ini

### emulator-console.log (tail)
INFO         | Android emulator version 37.2.12.0 (build_id 16428233) (CL:N/A)
INFO         | Graphics backend: gfxstream
INFO         | Found systemPath /usr/local/lib/android/sdk/system-images/android-34/google_apis/x86_64/
INFO         | Saving last run QEMU version for the AVD to 2
INFO         | Changing default hw.initialOrientation to portrait

INFO         | Increasing RAM size to 4096MB
##############################################################################
##                        WARNING - ACTION REQUIRED                         ##
##  Consider using the '-metrics-collection' flag to help improve the       ##
##  emulator by sending anonymized usage data. Or use the '-no-metrics'     ##
##  flag to bypass this warning and turn off the metrics collection.        ##
##  In a future release this warning will turn into a one-time blocking     ##
##  prompt to ask for explicit user input regarding metrics collection.     ##
##                                                                          ##
##  Please see '-help-metrics-collection' for more details. You can use     ##
##  '-metrics-to-file' or '-metrics-to-console' flags to see what type of   ##
##  data is being collected by emulator as part of usage statistics.        ##
##############################################################################
INFO         | Guest GLES Driver: Auto (ext controls)
INFO         | emuglConfig_init: vulkan_mode_selected:swiftshader gles_mode_selected:swiftshader
INFO         | Checking system compatibility:
INFO         |   Checking: hasSufficientDiskSpace
INFO         |      Ok: Disk space requirements to run avd: `gh_test` are met
INFO         |   Checking: hasSufficientHwGpu
INFO         |      Ok: Hardware GPU compatibility checks are not required
INFO         |   Checking: hasSufficientSystem
INFO         |      Warning: Suggested minimum system RAM to run avd 'gh_test' is 16384 MiB (available: 15989 MiB)
USER_WARNING | Suggested minimum system RAM to run avd 'gh_test' is 16384 MiB (available: 15989 MiB).
WARNING      | Feature QuickbootFileBacked is disabled due to stability issues, if you really want that, the environment variable ANDROID_EMU_FORCE_QUICKBOOT_FILE_BACKED need to set to 1
WARNING      | Failed to open /root/.android/adbkey
WARNING      | adbkey generation failed
INFO         | Storing crashdata in: /tmp/android-root/emu-crash-37.2.12.db, detection is enabled for process: 2856
INFO         | Initializing gfxstream backend
INFO         | startOpenglesRendererImpl: gpu info
INFO         | 
INFO         | Vulkan 1.4 is not supported for the guest and won't be enabled
INFO         | initIcdPaths: ICD set to 'swiftshader', using Swiftshader ICD
INFO         | Setting ICD filenames for the loader = /usr/local/lib/android/sdk/emulator/lib64/vulkan/vk_swiftshader_icd.json
INFO         | SharedLibrary::open for [/usr/local/lib/android/sdk/emulator/qemu/linux-x86_64/lib64/vulkan/libvulkan.so]
INFO         | SharedLibrary::open for [/usr/local/lib/android/sdk/emulator/qemu/linux-x86_64/lib64/vulkan/libvulkan.so.1]
INFO         | SharedLibrary::open for [/usr/local/lib/android/sdk/emulator/lib64/vulkan/libvulkan.so]
INFO         | Added library: /usr/local/lib/android/sdk/emulator/lib64/vulkan/libvulkan.so
INFO         | Selecting Vulkan device: SwiftShader Device (Subzero), Version: 1.3.0
INFO         | Using Vulkan externalMemoryMode: OpaqueFd for VkEmulation
INFO         | Format VK_FORMAT_G10X6_B10X6R10X6_2PLANE_422_UNORM_3PACK16 does not support YCbCr sampler conversion
INFO         | SharedLibrary::open for [libX11]
WARNING      | Could not open libX11.so, try libX11.so.6
INFO         | SharedLibrary::open for [libX11.so.6]
INFO         | SharedLibrary::open for [libX11-xcb]
WARNING      | Could not open libX11-xcb.so, try libX11-xcb.so.1
INFO         | SharedLibrary::open for [libX11-xcb.so.1]
INFO         | Initializing VkEmulation features:
INFO         |     glInteropSupported: false
INFO         |     useDeferredCommands: true
INFO         |     createResourceWithRequirements: true
INFO         |     useVulkanComposition: false
INFO         |     useVulkanNativeSwapchain: false
INFO         |     enable guestRenderDoc: false
INFO         |     ASTC LDR emulation mode: Gpu
INFO         |     enable ETC2 emulation: true
INFO         |     enable Ycbcr emulation: false
INFO         |     guestVulkanOnly: false
INFO         |     useDedicatedAllocations: false
INFO         |     guestVulkanMaxApiVersion: 1.3.0
INFO         |     enableProtectedMemoryEmulation: false
INFO         | Graphics Adapter Vendor Google (Google Inc.)
INFO         | Graphics Adapter Android Emulator OpenGL ES Translator (Google SwiftShader)
INFO         | Graphics API Version OpenGL ES 3.0 (OpenGL ES 3.0 SwiftShader 4.0.0.1)
INFO         | Graphics API Extensions GL_OES_EGL_sync GL_OES_EGL_image GL_OES_EGL_image_external GL_OES_depth24 GL_OES_depth32 GL_OES_element_index_uint GL_OES_texture_float GL_OES_texture_float_linear GL_OES_compressed_paletted_texture GL_OES_compressed_ETC1_RGB8_texture GL_OES_depth_texture GL_OES_texture_half_float GL_OES_texture_half_float_linear GL_OES_packed_depth_stencil GL_OES_vertex_half_float GL_OES_standard_derivatives GL_OES_texture_npot GL_OES_rgb8_rgba8 GL_EXT_color_buffer_float GL_EXT_color_buffer_half_float GL_EXT_texture_format_BGRA8888 GL_APPLE_texture_format_BGRA8888 
INFO         | Graphics Device Extensions N/A
INFO         | Disabling sparse binding feature support
WARNING      | No adb private key exists
INFO         | Userspace boot properties:
INFO         |   androidboot.boot_devices=pci0000:00/0000:00:03.0 pci0000:00/0000:00:06.0
INFO         |   androidboot.dalvik.vm.heapsize=576m
INFO         |   androidboot.debug.hwui.renderer=skiagl
INFO         |   androidboot.debug.sf.nobootanimation=1
INFO         |   androidboot.hardware=ranchu
INFO         |   androidboot.hardware.gltransport=pipe
INFO         |   androidboot.hardware.vulkan=ranchu
INFO         |   androidboot.logcat=*:V
INFO         |   androidboot.opengles.version=196608
INFO         |   androidboot.qemu=1
INFO         |   androidboot.qemu.avd_name=gh_test
INFO         |   androidboot.qemu.camera_hq_edge_processing=0
INFO         |   androidboot.qemu.camera_protocol_ver=1
INFO         |   androidboot.qemu.cpuvulkan.version=4210688
INFO         |   androidboot.qemu.gltransport.drawFlushInterval=800
INFO         |   androidboot.qemu.gltransport.name=pipe
INFO         |   androidboot.qemu.hwcodec.avcdec=2
INFO         |   androidboot.qemu.hwcodec.hevcdec=2
INFO         |   androidboot.qemu.hwcodec.vpxdec=2
INFO         |   androidboot.qemu.settings.system.screen_off_timeout=2147483647
INFO         |   androidboot.qemu.skin=1080x2400
INFO         |   androidboot.qemu.virtiowifi=1
INFO         |   androidboot.qemu.vsync=60
INFO         |   androidboot.serialno=EMULATOR37X2X12X0
INFO         |   androidboot.vbmeta.digest=451e57ed688ff746d2c636d52169ade253e2bc5bb30a5c3ff23679ca15d3bcd3
INFO         |   androidboot.vbmeta.hash_alg=sha256
INFO         |   androidboot.vbmeta.size=6656
INFO         |   androidboot.veritymode=enforcing
WARNING: cannnot unmap ptr 0x7f5c6e401000 as it is in the protected range from 0x7f5b6e400000 to 0x7f5c6e600000
pc_memory_init: above 4g size: 40000000
INFO         | Monitoring duration of emulator setup.
INFO         | Successfully initialized netsim WiFi
INFO         | Activated packet streamer for bluetooth emulation
INFO         | Setting display: 0 configuration to: 1080x2400, dpi: 420x420 
INFO         | setDisplayActiveConfig: id:0, 1080x2400
INFO         | emulatorSetupEnvironment: Environment scene is not required
USER_INFO    | Emulator is performing a full startup. This may take upto two minutes, or more.
WARNING      | Failed to process .ini file /root/.android/emu-update-last-check.ini for reading.
WARNING      | Failed to process .ini file /root/.android/emu-update-last-check.ini for reading.
INFO         | Boot completed in 31969 ms
INFO         | Increasing screen off timeout, logcat buffer size to 2M.
ERROR        | Failed to find ColorBuffer: 120
ERROR        | Failed to bind to texture: invalid color buffer.
INFO         | Wait for emulator (pid 2856) 20 seconds to shutdown gracefully before kill;you can set environment variable ANDROID_EMULATOR_WAIT_TIME_BEFORE_KILL(in seconds) to change the default value (20 seconds)

USER_INFO    | Snapshots have been disabled by the user, save request is ignored.
INFO         | Saving snapshot 'default_boot' took 0 ms
ERROR        | stop: Not implemented
WARNING      | Emulator client has not yet been configured.. Call configure me first!
INFO         | removeAll
WARNING      | Netsim Wifi dns:///localhost:39619 is gone due to Stream removed (CANCELLED)

### gradle-build.log (tail)
Downloading https://services.gradle.org/distributions/gradle-8.10.2-bin.zip
.............10%.............20%.............30%.............40%.............50%.............60%.............70%.............80%.............90%.............100%

Welcome to Gradle 8.10.2!

Here are the highlights of this release:
 - Support for Java 23
 - Faster configuration cache
 - Better configuration cache reports

For more details see https://docs.gradle.org/8.10.2/release-notes.html

To honour the JVM settings for this build a single-use Daemon process will be forked. For more on this, please refer to https://docs.gradle.org/8.10.2/userguide/gradle_daemon.html#sec:disabling_the_daemon in the Gradle documentation.
Daemon will be stopped at the end of the build 
Calculating task graph as no cached configuration is available for tasks: assembleDebug
> Task :app:checkKotlinGradlePluginConfigurationErrors SKIPPED
> Task :app:preBuild UP-TO-DATE
> Task :app:preDebugBuild UP-TO-DATE
> Task :app:mergeDebugNativeDebugMetadata NO-SOURCE
> Task :app:generateDebugResValues
> Task :app:createDebugCompatibleScreenManifests
> Task :app:generateDebugBuildConfig
> Task :app:extractDeepLinksDebug
> Task :app:generateDebugResources
> Task :app:mapDebugSourceSetPaths
> Task :app:checkDebugAarMetadata
> Task :app:javaPreCompileDebug
> Task :app:packageDebugResources
> Task :app:mergeDebugShaders
> Task :app:compileDebugShaders NO-SOURCE
> Task :app:generateDebugAssets UP-TO-DATE
> Task :app:processDebugMainManifest
> Task :app:processDebugManifest
> Task :app:processDebugManifestForPackage
> Task :app:desugarDebugFileDependencies
> Task :app:mergeDebugResources
> Task :app:mergeDebugJniLibFolders
> Task :app:parseDebugLocalResources
> Task :app:mergeDebugAssets
> Task :app:checkDebugDuplicateClasses
> Task :app:compressDebugAssets
> Task :app:mergeDebugNativeLibs

> Task :app:stripDebugDebugSymbols
Unable to strip the following libraries, packaging them as they are: libandroidx.graphics.path.so.

> Task :app:mergeLibDexDebug
> Task :app:writeDebugAppMetadata
> Task :app:writeDebugSigningConfigVersions
> Task :app:validateSigningDebug
> Task :app:processDebugResources
> Task :app:mergeExtDexDebug

> Task :app:compileDebugKotlin
w: file:///home/runner/work/Chat2DB/Chat2DB/gh-protocol/app/src/main/java/com/ghprotocol/app/MainActivity.kt:77:13 'fun updateConfiguration(p0: Configuration!, p1: DisplayMetrics!): Unit' is deprecated. Deprecated in Java.

> Task :app:processDebugJavaRes
> Task :app:mergeDebugJavaResource
> Task :app:compileDebugJavaWithJavac
> Task :app:dexBuilderDebug
> Task :app:mergeDebugGlobalSynthetics
> Task :app:mergeProjectDexDebug
> Task :app:packageDebug
> Task :app:assembleDebug
> Task :app:createDebugApkListingFileRedirect
gradle/actions: Writing build results to /home/runner/work/_temp/.gradle-actions/build-results/__run_3-1792923557094.json

BUILD SUCCESSFUL in 2m 13s
37 actionable tasks: 37 executed
Configuration cache entry stored.

### e2e.log
== adb devices ==
== wait for emulator to reach device state ==
emulator ready after ~4s
List of devices attached
emulator-5554	device

== install APK ==
Performing Streamed Install
Success
== probe emulator reachability to sub host (raw.githubusercontent.com:443, up to 20s) ==
emulator can reach raw.githubusercontent.com after ~12s
SUBMODE=live — app will fetch the subscription itself (full E2E)
== launch app (am start, up to 3 tries) ==
Starting: Intent { cmp=com.ghprotocol.app/.MainActivity }
app up (try 1, pid 3236)
== trigger connect via deep link ==
Starting: Intent { act=android.intent.action.VIEW dat=ghprotocol://connect/... }
== wait for tunnel; tap VPN consent when it appears (up to 6 min) ==
tunnel up after ~4s (xray pid + :10808 listener)
== wait for VpnService establish (consent result) ==
tapped VPN consent at: 894 1519 (iter vpn-1)
vpn established after ~6s
18: tun0: <POINTOPOINT,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UNKNOWN group default qlen 500
    link/none 
    inet 10.8.0.2/24 scope global tun0
       valid_lft forever preferred_lft forever
    inet6 fd00:1::1/128 scope global 
       valid_lft forever preferred_lft forever
    inet6 fe80::5ca8:116b:4209:4b1f/64 scope link stable-privacy 
       valid_lft forever preferred_lft forever
== DNS resolution THROUGH the tunnel (as app uid; toybox has no nslookup) ==
dns through tunnel: OK
Ping github.com (140.82.114.3): 56(84) bytes.

--- 140.82.114.3 ping statistics ---
1 packets transmitted, 0 received, 100% packet loss
== TCP through the tunnel (as app uid — data-path proof; toybox nc has no -z) ==
nc 1.1.1.1:443 -> rc=0
== relay diagnostics (GhVpnTunnel + GhDiag) ==
--------- beginning of main
10-25 10:23:12.701  3236  3236 D GhDiag  : connect: tap -> CHECKING (have sub=true)
10-25 10:23:12.701  3236  3236 D GhDiag  : connect: sub ok entries=2 -> PREPARING (core extract+version)
10-25 10:23:13.070  3236  3236 D GhDiag  : connect: ensureInstalled=true version=26.10.21 err=null
10-25 10:23:13.102  3236  3236 D GhDiag  : connect: config written bytes=5089 path=/data/user/0/com.ghprotocol.app/files/xray-config.json
10-25 10:23:13.293  3236  3236 D GhDiag  : connect: core.start=true 
10-25 10:23:19.206  3236  3236 D GhDiag  : tunnel: startTunnel called (running=false)
10-25 10:23:19.245  3236  3236 D GhDiag  : tunnel: established fd={ParcelFileDescriptor: java.io.FileDescriptor@2624a31} — relay loop started
10-25 10:23:19.691  3236  4528 D GhDiag  : tun pkt proto=6 dst=10.8.x.x len=64
10-25 10:23:19.721  3236  4545 D GhDiag  : relay tcp 10.8.x.x:853 -> socks5 ok
10-25 10:23:19.722  3236  4528 D GhDiag  : tun pkt proto=6 dst=10.8.x.x len=40
10-25 10:23:19.722  3236  4528 D GhDiag  : tun pkt proto=6 dst=10.8.x.x len=270
10-25 10:23:19.724  3236  4528 D GhDiag  : tun pkt proto=6 dst=10.8.x.x len=60
10-25 10:23:19.727  3236  4528 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=61
10-25 10:23:19.727  3236  4528 D GhDiag  : tun pkt proto=6 dst=10.8.x.x len=60
10-25 10:23:19.747  3236  4528 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=61
10-25 10:23:19.748  3236  4528 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=78
10-25 10:23:19.756  3236  4528 D GhDiag  : tun pkt proto=6 dst=5.61.x.x len=120
10-25 10:23:19.777  3236  4528 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=78
10-25 10:23:19.778  3236  4528 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=78
10-25 10:23:19.787  3236  4528 D GhDiag  : tun pkt proto=6 dst=5.61.x.x len=64
10-25 10:23:19.793  3236  4528 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=77
10-25 10:23:19.793  3236  4528 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=77
10-25 10:23:19.857  3236  4528 D GhDiag  : tun pkt proto=6 dst=10.8.x.x len=60
10-25 10:23:20.027  3236  4528 D GhDiag  : tun pkt proto=1 dst=172.217.x.x len=28
10-25 10:23:20.055  3236  4528 D GhDiag  : tun pkt proto=17 dst=172.217.x.x len=216
10-25 10:23:20.056  3236  4528 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=61
10-25 10:23:20.056  3236  4528 D GhDiag  : tun pkt proto=17 dst=172.217.x.x len=893
10-25 10:23:20.058  3236  4528 D GhDiag  : tun pkt proto=6 dst=10.8.x.x len=60
10-25 10:23:21.388  3236  4552 D GhDiag  : relay dns -> 178B ok
10-25 10:23:21.390  3236  4556 D GhDiag  : relay dns -> 177B ok
10-25 10:23:21.390  3236  4551 D GhDiag  : relay dns -> 274B ok
10-25 10:23:21.390  3236  4555 D GhDiag  : relay dns -> 273B ok
10-25 10:23:23.867  3236  4657 D GhDiag  : relay dns -> 93B ok
10-25 10:23:23.871  3236  4659 D GhDiag  : relay dns -> 44B ok
10-25 10:23:25.266  3236  4676 D GhDiag  : relay dns -> 164B ok
10-25 10:23:25.267  3236  4678 D GhDiag  : relay dns -> 260B ok
10-25 10:23:25.573  3236  4686 D GhDiag  : relay tcp 172.217.x.x:443 -> socks5 ok
10-25 10:23:25.817  3236  4687 D GhDiag  : relay tcp 172.217.x.x:443 -> socks5 ok
10-25 10:23:25.904  3236  4692 D GhDiag  : relay tcp 1.1.x.x:443 -> socks5 ok
== HTTPS probe through tunnel (best-effort) ===
no curl on emulator — skipping HTTPS probe (TCP + DNS are the core signal)
== Xray core stderr (from app filesDir) ==
== logcat sanity (crashes + GhVpnTunnel) ==
--------- beginning of main
10-25 10:23:12.701  3236  3236 D GhDiag  : connect: tap -> CHECKING (have sub=true)
10-25 10:23:12.701  3236  3236 D GhDiag  : connect: sub ok entries=2 -> PREPARING (core extract+version)
10-25 10:23:13.070  3236  3236 D GhDiag  : connect: ensureInstalled=true version=26.10.21 err=null
10-25 10:23:13.102  3236  3236 D GhDiag  : connect: config written bytes=5089 path=/data/user/0/com.ghprotocol.app/files/xray-config.json
10-25 10:23:13.293  3236  3236 D GhDiag  : connect: core.start=true 
10-25 10:23:19.206  3236  3236 D GhDiag  : tunnel: startTunnel called (running=false)
10-25 10:23:19.245  3236  3236 D GhDiag  : tunnel: established fd={ParcelFileDescriptor: java.io.FileDescriptor@2624a31} — relay loop started
10-25 10:23:19.691  3236  4528 D GhDiag  : tun pkt proto=6 dst=10.8.x.x len=64
10-25 10:23:19.721  3236  4545 D GhDiag  : relay tcp 10.8.x.x:853 -> socks5 ok
10-25 10:23:19.722  3236  4528 D GhDiag  : tun pkt proto=6 dst=10.8.x.x len=40
10-25 10:23:19.722  3236  4528 D GhDiag  : tun pkt proto=6 dst=10.8.x.x len=270
10-25 10:23:19.724  3236  4528 D GhDiag  : tun pkt proto=6 dst=10.8.x.x len=60
10-25 10:23:19.727  3236  4528 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=61
10-25 10:23:19.727  3236  4528 D GhDiag  : tun pkt proto=6 dst=10.8.x.x len=60
10-25 10:23:19.747  3236  4528 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=61
10-25 10:23:19.748  3236  4528 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=78
10-25 10:23:19.756  3236  4528 D GhDiag  : tun pkt proto=6 dst=5.61.x.x len=120
10-25 10:23:19.777  3236  4528 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=78
10-25 10:23:19.778  3236  4528 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=78
10-25 10:23:19.787  3236  4528 D GhDiag  : tun pkt proto=6 dst=5.61.x.x len=64
10-25 10:23:19.793  3236  4528 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=77
10-25 10:23:19.793  3236  4528 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=77
10-25 10:23:19.857  3236  4528 D GhDiag  : tun pkt proto=6 dst=10.8.x.x len=60
10-25 10:23:20.027  3236  4528 D GhDiag  : tun pkt proto=1 dst=172.217.x.x len=28
10-25 10:23:20.055  3236  4528 D GhDiag  : tun pkt proto=17 dst=172.217.x.x len=216
10-25 10:23:20.056  3236  4528 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=61
10-25 10:23:20.056  3236  4528 D GhDiag  : tun pkt proto=17 dst=172.217.x.x len=893
10-25 10:23:20.058  3236  4528 D GhDiag  : tun pkt proto=6 dst=10.8.x.x len=60
10-25 10:23:21.388  3236  4552 D GhDiag  : relay dns -> 178B ok
10-25 10:23:21.390  3236  4556 D GhDiag  : relay dns -> 177B ok
10-25 10:23:21.390  3236  4551 D GhDiag  : relay dns -> 274B ok
10-25 10:23:21.390  3236  4555 D GhDiag  : relay dns -> 273B ok
10-25 10:23:23.867  3236  4657 D GhDiag  : relay dns -> 93B ok
10-25 10:23:23.871  3236  4659 D GhDiag  : relay dns -> 44B ok
10-25 10:23:25.266  3236  4676 D GhDiag  : relay dns -> 164B ok
10-25 10:23:25.267  3236  4678 D GhDiag  : relay dns -> 260B ok
10-25 10:23:25.573  3236  4686 D GhDiag  : relay tcp 172.217.x.x:443 -> socks5 ok
10-25 10:23:25.817  3236  4687 D GhDiag  : relay tcp 172.217.x.x:443 -> socks5 ok
10-25 10:23:25.904  3236  4692 D GhDiag  : relay tcp 1.1.x.x:443 -> socks5 ok
===============================
E2E PASS: real tunnel carrying traffic (SUBMODE=live)
  - core install + start: verified (Xray 26.10.21 exec from nativeLibraryDir)
  - VpnService establish: verified (consent tapped: 1, vpnUp: 1)
  - SOCKS5 data path: verified (tcp=1)
  - DNS through tunnel: verified
===============================


### e2e-logcat.log (crashes + app + vpn, tail)
protocol.app
10-25 10:23:03.220  1579  1579 I AiAiEcho: AppFetcherImplV2 updateApps package:[com.ghprotocol.app], userId:[0], reason:[package is added.].
10-25 10:23:03.230  1579  1579 I AiAiEcho: AppFetcherImpl onPackageChanged com.ghprotocol.app.
10-25 10:23:03.240  1579  2806 I AiAiEcho: AppIndexer Package:[com.ghprotocol.app] UserProfile:[0] Enabled:[true].
10-25 10:23:03.240  1579  2806 I AiAiEcho: AppFetcherImplV2 updateApps package:[com.ghprotocol.app], userId:[0], reason:[package is updated.].
10-25 10:23:04.062   521  2295 V SplashScreenExceptionList: SplashScreen checking exception for package com.ghprotocol.app (target sdk:35) -> false
10-25 10:23:04.064   521  2295 I ActivityTaskManager: START u0 {flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity} with LAUNCH_MULTIPLE from uid 2000 (BAL_ALLOW_PERMISSION) result code=0
10-25 10:23:04.138   834   865 V WindowManagerShell: Transition requested: android.os.BinderProxy@ab448de TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=1 lastActiveTime=39678 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{android.window.IWindowContainerToken$Stub$Proxy@6aadabf} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{41f858c com.ghprotocol.app.MainActivity} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=false isVisible=false isVisibleRequested=false isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-25 10:23:04.153   521  2448 D CoreBackPreview: Window{7032ca7 u0 Splash Screen com.ghprotocol.app}: Setting back callback OnBackInvokedCallbackInfo{mCallback=android.window.IOnBackInvokedCallback$Stub$Proxy@cb3dcfd, mPriority=0, mIsAnimationCallback=false}
10-25 10:23:04.322   521   549 I ActivityManager: Start proc 3236:com.ghprotocol.app/u0a192 for next-top-activity {com.ghprotocol.app/com.ghprotocol.app.MainActivity}
10-25 10:23:04.533  3236  3236 I .ghprotocol.app: Late-enabling -Xcheck:jni
10-25 10:23:04.557  3236  3236 I .ghprotocol.app: Using CollectorTypeCC GC.
10-25 10:23:04.557  3236  3236 W .ghprotocol.app: Unexpected CPU variant for x86: x86_64.
10-25 10:23:04.557  3236  3236 W .ghprotocol.app: Known variants: atom, sandybridge, silvermont, goldmont, goldmont-plus, tremont, kabylake, default
10-25 10:23:04.683   521   571 I AppsFilter: interaction: PackageSetting{7599d86 com.ghprotocol.app/10192} -> PackageSetting{acb1647 com.google.android.youtube/10139} BLOCKED
10-25 10:23:04.683   521   571 I AppsFilter: interaction: PackageSetting{7599d86 com.ghprotocol.app/10192} -> PackageSetting{b2c4e74 com.google.android.googlequicksearchbox/10132} BLOCKED
10-25 10:23:04.683   521   571 I AppsFilter: interaction: PackageSetting{7599d86 com.ghprotocol.app/10192} -> PackageSetting{37cef9d com.google.android.as/10126} BLOCKED
10-25 10:23:04.683   521   571 I AppsFilter: interaction: PackageSetting{7599d86 com.ghprotocol.app/10192} -> PackageSetting{da20c12 com.google.android.gm/10142} BLOCKED
10-25 10:23:04.683   521   571 I AppsFilter: interaction: PackageSetting{7599d86 com.ghprotocol.app/10192} -> PackageSetting{598cfe3 com.google.android.devicelockcontroller/10180} BLOCKED
10-25 10:23:04.683   521   571 I AppsFilter: interaction: PackageSetting{7599d86 com.ghprotocol.app/10192} -> PackageSetting{df9dde0 com.google.android.dialer/10128} BLOCKED
10-25 10:23:04.683   521   571 I AppsFilter: interaction: PackageSetting{7599d86 com.ghprotocol.app/10192} -> PackageSetting{3de899 com.google.android.contacts/10153} BLOCKED
10-25 10:23:04.683   521   571 I AppsFilter: interaction: PackageSetting{7599d86 com.ghprotocol.app/10192} -> PackageSetting{690d75e com.google.android.partnersetup/10124} BLOCKED
10-25 10:23:04.683   521   571 I AppsFilter: interaction: PackageSetting{7599d86 com.ghprotocol.app/10192} -> PackageSetting{dfe873f com.google.android.apps.youtube.music/10156} BLOCKED
10-25 10:23:04.684   521   571 I AppsFilter: interaction: PackageSetting{7599d86 com.ghprotocol.app/10192} -> PackageSetting{c4ef80c com.google.android.cellbroadcastreceiver/10189} BLOCKED
10-25 10:23:04.684   521   571 I AppsFilter: interaction: PackageSetting{7599d86 com.ghprotocol.app/10192} -> PackageSetting{27b7555 com.google.android.inputmethod.latin/10140} BLOCKED
10-25 10:23:04.926   521   538 V WindowManager: Sent Transition #6 createdAt=10-25 10:23:04.050 via request=TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=1 lastActiveTime=39678 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{RemoteToken{c1c121e Task{e120cf4 #8 type=standard A=10192:com.ghprotocol.app}}} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{6ad0aff com.ghprotocol.app.MainActivity} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=false isVisible=false isVisibleRequested=false isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-25 10:23:04.926   521   538 V WindowManager:     info={id=6 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{WCT{RemoteToken{c1c121e Task{e120cf4 #8 type=standard A=10192:com.ghprotocol.app}}} m=OPEN f=NONE leash=Surface(name=Task=8)/@0x3306aa0 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0},{WCT{RemoteToken{14190cc Task{972c7c9 #1 type=home}}} m=TO_BACK f=SHOW_WALLPAPER leash=Surface(name=Task=1)/@0x49ebf09 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-25 10:23:04.973  3236  3236 W ziparchive: Unable to open '/data/app/~~Z0y8aSKC9d0Hx6TUvv5hLg==/com.ghprotocol.app-xtjPud9g8suTKeNtCByfuA==/base.dm': No such file or directory
10-25 10:23:04.975  3236  3236 W ziparchive: Unable to open '/data/app/~~Z0y8aSKC9d0Hx6TUvv5hLg==/com.ghprotocol.app-xtjPud9g8suTKeNtCByfuA==/base.dm': No such file or directory
10-25 10:23:05.538  3236  3236 D nativeloader: Configuring clns-6 for other apk /data/app/~~Z0y8aSKC9d0Hx6TUvv5hLg==/com.ghprotocol.app-xtjPud9g8suTKeNtCByfuA==/base.apk. target_sdk_version=35, uses_libraries=, library_path=/data/app/~~Z0y8aSKC9d0Hx6TUvv5hLg==/com.ghprotocol.app-xtjPud9g8suTKeNtCByfuA==/lib/x86_64:/data/app/~~Z0y8aSKC9d0Hx6TUvv5hLg==/com.ghprotocol.app-xtjPud9g8suTKeNtCByfuA==/base.apk!/lib/x86_64, permitted_path=/data:/mnt/expand:/data/user/0/com.ghprotocol.app
10-25 10:23:05.545  3236  3236 V GraphicsEnvironment: ANGLE GameManagerService for com.ghprotocol.app: false
10-25 10:23:05.545  3236  3236 V GraphicsEnvironment: com.ghprotocol.app is not listed in per-application setting
10-25 10:23:06.963  3236  3236 W .ghprotocol.app: Method boolean androidx.compose.runtime.snapshots.SnapshotStateList.conditionalUpdate(boolean, kotlin.jvm.functions.Function1) failed lock verification and will run slower.
10-25 10:23:06.963  3236  3236 W .ghprotocol.app: Common causes for lock verification issues are non-optimized dex code
10-25 10:23:06.963  3236  3236 W .ghprotocol.app: and incorrect proguard optimizations.
10-25 10:23:06.964  3236  3236 W .ghprotocol.app: Method boolean androidx.compose.runtime.snapshots.SnapshotStateList.conditionalUpdate$default(androidx.compose.runtime.snapshots.SnapshotStateList, boolean, kotlin.jvm.functions.Function1, int, java.lang.Object) failed lock verification and will run slower.
10-25 10:23:06.964  3236  3236 W .ghprotocol.app: Method java.lang.Object androidx.compose.runtime.snapshots.SnapshotStateList.mutate(kotlin.jvm.functions.Function1) failed lock verification and will run slower.
10-25 10:23:06.964  3236  3236 W .ghprotocol.app: Method void androidx.compose.runtime.snapshots.SnapshotStateList.update(boolean, kotlin.jvm.functions.Function1) failed lock verification and will run slower.
10-25 10:23:06.964  3236  3236 W .ghprotocol.app: Method void androidx.compose.runtime.snapshots.SnapshotStateList.update$default(androidx.compose.runtime.snapshots.SnapshotStateList, boolean, kotlin.jvm.functions.Function1, int, java.lang.Object) failed lock verification and will run slower.
10-25 10:23:07.055   521  2423 D CoreBackPreview: Window{e19ce50 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}: Setting back callback OnBackInvokedCallbackInfo{mCallback=android.window.IOnBackInvokedCallback$Stub$Proxy@c2584f2, mPriority=0, mIsAnimationCallback=false}
10-25 10:23:08.135   521   538 W ziparchive: Unable to open '/data/app/~~Z0y8aSKC9d0Hx6TUvv5hLg==/com.ghprotocol.app-xtjPud9g8suTKeNtCByfuA==/base.dm': No such file or directory
10-25 10:23:08.135   521   538 I ActivityTaskManager: Displayed com.ghprotocol.app/.MainActivity for user 0: +4s89ms
10-25 10:23:08.173   521  2419 W InputManager-JNI: Input channel object '7032ca7 Splash Screen com.ghprotocol.app (client)' was disposed without first being removed with the input manager!
10-25 10:23:08.564   521  2417 I ImeTracker: com.ghprotocol.app:5371b03f: onRequestHide at ORIGIN_SERVER_HIDE_INPUT reason HIDE_UNSPECIFIED_WINDOW
10-25 10:23:08.564   521  2417 I ImeTracker: com.ghprotocol.app:5371b03f: onCancelled at PHASE_SERVER_SHOULD_HIDE
10-25 10:23:08.587  1497  1497 I GoogleInputMethodService: GoogleInputMethodService.onStartInput():1877 onStartInput(EditorInfo{inputType=0x0(NULL) imeOptions=0x0 privateImeOptions=null actionName=UNSPECIFIED actionLabel=null actionId=0 initialSelStart=-1 initialSelEnd=-1 initialCapsMode=0x0 hintText=null label=null packageName=com.ghprotocol.app fieldId=0 fieldName=null extras=null}, false)
10-25 10:23:11.042   521   912 I AppsFilter: interaction: PackageSetting{7599d86 com.ghprotocol.app/10192} -> PackageSetting{fa1cca0 com.google.android.gm/10142} BLOCKED
10-25 10:23:11.588  3236  3900 D ProfileInstaller: Installing profile for com.ghprotocol.app
10-25 10:23:12.332   521  2417 I ActivityTaskManager: START u0 {act=android.intent.action.VIEW dat=ghprotocol://connect/... flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity} with LAUNCH_MULTIPLE from uid 2000 (BAL_ALLOW_PERMISSION) result code=0
10-25 10:23:12.336   834   865 V WindowManagerShell: Transition requested: android.os.BinderProxy@165c800 TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=2 lastActiveTime=47947 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{android.window.IWindowContainerToken$Stub$Proxy@b465839} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{eb1e7e com.ghprotocol.app.MainActivity} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=true isVisible=true isVisibleRequested=true isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-25 10:23:12.348   521  2295 I AppsFilter: interaction: PackageSetting{7599d86 com.ghprotocol.app/10192} -> PackageSetting{4bd64e9 com.google.android.settings.intelligence/10118} BLOCKED
10-25 10:23:12.352   521  1878 I AppsFilter: interaction: PackageSetting{7599d86 com.ghprotocol.app/10192} -> PackageSetting{1b0a40f com.google.android.settings.intelligence/10118} BLOCKED
10-25 10:23:12.624  4024  4024 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-25 10:23:12.637  4024  4024 I AndroidRuntime: Using default boot image
10-25 10:23:12.639  4024  4024 I AndroidRuntime: Leaving lock profiling enabled
10-25 10:23:12.701  3236  3236 D GhDiag  : connect: tap -> CHECKING (have sub=true)
10-25 10:23:12.701  3236  3236 D GhDiag  : connect: sub ok entries=2 -> PREPARING (core extract+version)
10-25 10:23:12.734  4065  4065 W libxraycore.so: type=1400 audit(0.0:15): avc:  denied  { search } for  name="tests" dev="dm-40" ino=65540 scontext=u:r:untrusted_app:s0:c192,c256,c512,c768 tcontext=u:object_r:shell_test_data_file:s0 tclass=dir permissive=0 app=com.ghprotocol.app
10-25 10:23:12.734  4065  4065 W libxraycore.so: type=1400 audit(0.0:16): avc:  denied  { search } for  name="tests" dev="dm-40" ino=65540 scontext=u:r:untrusted_app:s0:c192,c256,c512,c768 tcontext=u:object_r:shell_test_data_file:s0 tclass=dir permissive=0 app=com.ghprotocol.app
10-25 10:23:12.734  4065  4065 W libxraycore.so: type=1400 audit(0.0:17): avc:  denied  { search } for  name="tests" dev="dm-40" ino=65540 scontext=u:r:untrusted_app:s0:c192,c256,c512,c768 tcontext=u:object_r:shell_test_data_file:s0 tclass=dir permissive=0 app=com.ghprotocol.app
10-25 10:23:12.734  4065  4065 W libxraycore.so: type=1400 audit(0.0:18): avc:  denied  { search } for  name="tests" dev="dm-40" ino=65540 scontext=u:r:untrusted_app:s0:c192,c256,c512,c768 tcontext=u:object_r:shell_test_data_file:s0 tclass=dir permissive=0 app=com.ghprotocol.app
10-25 10:23:12.950  1441  3464 I BlockstoreStorage: Clearing Blockstore Data for package com.ghprotocol.app [CONTEXT service_id=258 ]
10-25 10:23:13.003  4024  4024 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-25 10:23:13.070  3236  3236 D GhDiag  : connect: ensureInstalled=true version=26.10.21 err=null
10-25 10:23:13.102  3236  3236 D GhDiag  : connect: config written bytes=5089 path=/data/user/0/com.ghprotocol.app/files/xray-config.json
10-25 10:23:13.293  3236  3236 D GhDiag  : connect: core.start=true 
10-25 10:23:13.359   521   914 D CoreBackPreview: Window{5607af6 u0 com.ghprotocol.app/com.ghprotocol.app.MainActivity}: Setting back callback OnBackInvokedCallbackInfo{mCallback=android.window.IOnBackInvokedCallback$Stub$Proxy@cf94bca, mPriority=0, mIsAnimationCallback=false}
10-25 10:23:13.639  1402  2776 I FontLog : Package com.ghprotocol.app has no metadata [CONTEXT service_id=132 ]
10-25 10:23:14.176  4024  4024 D AndroidRuntime: Shutting down VM
10-25 10:23:14.225   834   865 V WindowManagerShell: onTransitionReady android.os.BinderProxy@165c800: {id=7 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{null m=OPEN f=FILLS_TASK leash=Surface(name=ActivityRecord{f069922 u0 com.ghprotocol.app/.MainActivity)/@0x83dd571 sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=TO_BACK f=FILLS_TASK leash=Surface(name=ActivityRecord{fcebec7 u0 com.ghprotocol.app/.MainActivity)/@0xfc27f56 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-25 10:23:14.225   521   538 I ActivityTaskManager: Displayed com.ghprotocol.app/.MainActivity for user 0: +1s914ms
10-25 10:23:14.226   521   538 V WindowManager: Sent Transition #7 createdAt=10-25 10:23:12.328 via request=TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=2 lastActiveTime=47947 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{RemoteToken{c1c121e Task{e120cf4 #8 type=standard A=10192:com.ghprotocol.app}}} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{8e86184 com.ghprotocol.app.MainActivity} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=true isVisible=true isVisibleRequested=true isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-25 10:23:14.226   521   538 V WindowManager:     info={id=7 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{null m=OPEN f=FILLS_TASK leash=Surface(name=ActivityRecord{f069922 u0 com.ghprotocol.app/.MainActivity)/@0x4028f31 sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=TO_BACK f=FILLS_TASK leash=Surface(name=ActivityRecord{fcebec7 u0 com.ghprotocol.app/.MainActivity)/@0x3551fd8 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-25 10:23:14.227   834   865 V WindowManagerShell: Transition doesn't have explicit remote, search filters for match for {id=7 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{null m=OPEN f=FILLS_TASK leash=Surface(name=ActivityRecord{f069922 u0 com.ghprotocol.app/.MainActivity)/@0x83dd571 sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=TO_BACK f=FILLS_TASK leash=Surface(name=ActivityRecord{fcebec7 u0 com.ghprotocol.app/.MainActivity)/@0xfc27f56 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-25 10:23:14.227   834   865 V WindowManagerShell: start default transition animation, info = {id=7 t=OPEN f=0x0 trk=0 r=[0@Point(0, 0)] c=[{null m=OPEN f=FILLS_TASK leash=Surface(name=ActivityRecord{f069922 u0 com.ghprotocol.app/.MainActivity)/@0x83dd571 sb=Rect(0, 0 - 0, 0) eb=Rect(0, 0 - 1080, 2400) d=-1->0 r=-1->0:-1},{null m=TO_BACK f=FILLS_TASK leash=Surface(name=ActivityRecord{fcebec7 u0 com.ghprotocol.app/.MainActivity)/@0xfc27f56 sb=Rect(0, 0 - 1080, 2400) eb=Rect(0, 0 - 1080, 2400) d=0}]}
10-25 10:23:14.254  4128  4128 W libxraycore.so: type=1400 audit(0.0:30): avc:  denied  { read } for  name="somaxconn" dev="proc" ino=56748 scontext=u:r:untrusted_app:s0:c192,c256,c512,c768 tcontext=u:object_r:proc_net:s0 tclass=file permissive=0 app=com.ghprotocol.app
10-25 10:23:14.724   834   865 V WindowManagerShell: Transition requested: android.os.BinderProxy@247f648 TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.android.vpndialogs/com.android.vpndialogs.ConfirmDialog} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=3 lastActiveTime=49928 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{android.window.IWindowContainerToken$Stub$Proxy@95dfce1} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{7176a06 com.android.vpndialogs.ConfirmDialog} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=true isVisible=true isVisibleRequested=true isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-25 10:23:14.760   521   590 I ImeTracker: com.ghprotocol.app:78f1129f: onRequestHide at ORIGIN_SERVER_HIDE_INPUT reason HIDE_UNSPECIFIED_WINDOW
10-25 10:23:14.760   521   590 I ImeTracker: com.ghprotocol.app:78f1129f: onCancelled at PHASE_SERVER_SHOULD_HIDE
10-25 10:23:14.778  1497  1497 I GoogleInputMethodService: GoogleInputMethodService.onStartInput():1877 onStartInput(EditorInfo{inputType=0x0(NULL) imeOptions=0x0 privateImeOptions=null actionName=UNSPECIFIED actionLabel=null actionId=0 initialSelStart=-1 initialSelEnd=-1 initialCapsMode=0x0 hintText=null label=null packageName=com.ghprotocol.app fieldId=0 fieldName=null extras=null}, false)
10-25 10:23:14.994   521  2447 E AppOps  : Bad call made by uid 10097. Package "com.ghprotocol.app" does not belong to uid 10097.
10-25 10:23:14.999   521  2447 E AppOps  : java.lang.SecurityException: Specified package "com.ghprotocol.app" under uid 10097 but it is not
10-25 10:23:14.999   521  2447 E AppOps  : 	at com.android.server.connectivity.Vpn.isVpnServicePreConsented(Vpn.java:1543)
10-25 10:23:15.744   521   571 I AppsFilter: interaction: PackageSetting{7599d86 com.ghprotocol.app/10192} -> PackageSetting{4046fe0 com.google.android.googlequicksearchbox/10132} BLOCKED
10-25 10:23:15.745   521   571 I AppsFilter: interaction: PackageSetting{7599d86 com.ghprotocol.app/10192} -> PackageSetting{73a1299 com.android.camera2/10147} BLOCKED
10-25 10:23:15.745   521   571 I AppsFilter: interaction: PackageSetting{7599d86 com.ghprotocol.app/10192} -> PackageSetting{bab95e com.google.android.gm/10142} BLOCKED
10-25 10:23:15.745   521   571 I AppsFilter: interaction: PackageSetting{7599d86 com.ghprotocol.app/10192} -> PackageSetting{afc13f com.google.android.devicelockcontroller/10180} BLOCKED
10-25 10:23:15.745   521   571 I AppsFilter: interaction: PackageSetting{7599d86 com.ghprotocol.app/10192} -> PackageSetting{d70aa0c com.google.android.rkpdapp/10188} BLOCKED
10-25 10:23:15.745   521   571 I AppsFilter: interaction: PackageSetting{7599d86 com.ghprotocol.app/10192} -> PackageSetting{e103f55 com.google.android.settings.intelligence/10118} BLOCKED
10-25 10:23:15.745   521   571 I AppsFilter: interaction: PackageSetting{7599d86 com.ghprotocol.app/10192} -> PackageSetting{67811e9 com.google.android.projection.gearhead/10123} BLOCKED
10-25 10:23:16.124   521   538 V WindowManager: Sent Transition #8 createdAt=10-25 10:23:14.296 via request=TransitionRequestInfo { type = OPEN, triggerTask = TaskInfo{userId=0 taskId=8 displayId=0 isRunning=true baseIntent=Intent { flg=0x10000000 cmp=com.ghprotocol.app/.MainActivity } baseActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} topActivity=ComponentInfo{com.android.vpndialogs/com.android.vpndialogs.ConfirmDialog} origActivity=null realActivity=ComponentInfo{com.ghprotocol.app/com.ghprotocol.app.MainActivity} numActivities=3 lastActiveTime=49928 supportsMultiWindow=true resizeMode=1 isResizeable=true minWidth=-1 minHeight=-1 defaultMinSize=220 token=WCT{RemoteToken{c1c121e Task{e120cf4 #8 type=standard A=10192:com.ghprotocol.app}}} topActivityType=1 pictureInPictureParams=null shouldDockBigOverlays=false launchIntoPipHostTaskId=-1 lastParentTaskIdBeforePip=-1 displayCutoutSafeInsets=null topActivityInfo=ActivityInfo{8770134 com.android.vpndialogs.ConfirmDialog} launchCookies=[] positionInParent=Point(0, 0) parentTaskId=-1 isFocused=true isVisible=true isVisibleRequested=true isSleeping=false topActivityInSizeCompat=false topActivityEligibleForLetterboxEducation= false topActivityLetterboxed= false isFromDoubleTap= false topActivityLetterboxVerticalPosition= -1 topActivityLetterboxHorizontalPosition= -1 topActivityLetterboxWidth=-1 topActivityLetterboxHeight=-1 locusId=null displayAreaFeatureId=1 cameraCompatControlState=hidden}, remoteTransition = null, displayChange = null }
10-25 10:23:16.250  3236  3256 W .ghprotocol.app: Suspending all threads took: 40.234ms
10-25 10:23:16.253  3236  3256 I .ghprotocol.app: Background concurrent copying GC freed 93849(4998KB) AllocSpace objects, 26(740KB) LOS objects, 49% free, 6881KB/13MB, paused 34us,40.446ms total 1.675s
10-25 10:23:16.302  4272  4272 D AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<
10-25 10:23:16.311  4272  4272 I AndroidRuntime: Using default boot image
10-25 10:23:16.311  4272  4272 I AndroidRuntime: Leaving lock profiling enabled
10-25 10:23:16.527  4272  4272 D AndroidRuntime: Calling main entry com.android.commands.uiautomator.Launcher
10-25 10:23:18.064  4272  4272 D AndroidRuntime: Shutting down VM
10-25 10:23:19.170   521  2030 I Vpn     : Switched from [Legacy VPN] to com.ghprotocol.app
10-25 10:23:19.205   521  2295 I ActivityManager: Background started FGS: Allowed [callingPackage: com.ghprotocol.app; callingUid: 10192; uidState: TOP ; uidBFSL: [BFSL]; intent: Intent { cmp=com.ghprotocol.app/.core.VpnTunnelService }; code:PROC_STATE_TOP; tempAllowListReason:<null>; targetSdkVersion:35; callerTargetSdkVersion:35; startForegroundCount:0; bindFromPackage:null: isBindService:false]
10-25 10:23:19.206  3236  3236 D GhDiag  : tunnel: startTunnel called (running=false)
10-25 10:23:19.245   521  2127 I Vpn     : Established by com.ghprotocol.app on tun0
10-25 10:23:19.245  3236  3236 D GhDiag  : tunnel: established fd={ParcelFileDescriptor: java.io.FileDescriptor@2624a31} — relay loop started
10-25 10:23:19.517   521  2419 I ImeTracker: com.ghprotocol.app:9c4e484d: onRequestHide at ORIGIN_SERVER_HIDE_INPUT reason HIDE_SAME_WINDOW_FOCUSED_WITHOUT_EDITOR
10-25 10:23:19.517   521  2419 I ImeTracker: com.ghprotocol.app:9c4e484d: onCancelled at PHASE_SERVER_SHOULD_HIDE
10-25 10:23:19.524  1497  1497 I GoogleInputMethodService: GoogleInputMethodService.onStartInput():1877 onStartInput(EditorInfo{inputType=0x0(NULL) imeOptions=0x0 privateImeOptions=null actionName=UNSPECIFIED actionLabel=null actionId=0 initialSelStart=-1 initialSelEnd=-1 initialCapsMode=0x0 hintText=null label=null packageName=com.ghprotocol.app fieldId=0 fieldName=null extras=null}, false)
10-25 10:23:19.691  3236  4528 D GhDiag  : tun pkt proto=6 dst=10.8.x.x len=64
10-25 10:23:19.721  3236  4545 D GhDiag  : relay tcp 10.8.x.x:853 -> socks5 ok
10-25 10:23:19.722  3236  4528 D GhDiag  : tun pkt proto=6 dst=10.8.x.x len=40
10-25 10:23:19.722  3236  4528 D GhDiag  : tun pkt proto=6 dst=10.8.x.x len=270
10-25 10:23:19.724  3236  4528 D GhDiag  : tun pkt proto=6 dst=10.8.x.x len=60
10-25 10:23:19.727  3236  4528 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=61
10-25 10:23:19.727  3236  4528 D GhDiag  : tun pkt proto=6 dst=10.8.x.x len=60
10-25 10:23:19.747  3236  4528 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=61
10-25 10:23:19.748  3236  4528 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=78
10-25 10:23:19.756  3236  4528 D GhDiag  : tun pkt proto=6 dst=5.61.x.x len=120
10-25 10:23:19.777  3236  4528 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=78
10-25 10:23:19.778  3236  4528 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=78
10-25 10:23:19.787  3236  4528 D GhDiag  : tun pkt proto=6 dst=5.61.x.x len=64
10-25 10:23:19.793  3236  4528 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=77
10-25 10:23:19.793  3236  4528 D GhDiag  : tun pkt proto=17 dst=10.8.x.x len=77
10-25 10:23:19.857  3236  4528 D GhDiag  : tun pkt proto=6 dst=10.8.x.x len=60
10-25 10:23:20.027  3236  4528 D GhDiag  : tun pkt proto=1 dst=172.217.x.x len=28
10-25 10:23:20.055  3236  4528 D GhDiag  : tun pkt proto=17 dst=172.217.x.x len=216
10-25 10:23:20.056  3236  4528 D GhDiag  : tun pkt proto=17 dst=142.251.x.x len=61
10-25 10:23:20.056  3236  4528 D GhDiag  : tun pkt proto=17 dst=172.217.x.x len=893
10-25 10:23:20.058  3236  4528 D GhDiag  : tun pkt proto=6 dst=10.8.x.x len=60
10-25 10:23:21.388  3236  4552 D GhDiag  : relay dns -> 178B ok
10-25 10:23:21.390  3236  4556 D GhDiag  : relay dns -> 177B ok
10-25 10:23:21.390  3236  4551 D GhDiag  : relay dns -> 274B ok
10-25 10:23:21.390  3236  4555 D GhDiag  : relay dns -> 273B ok
10-25 10:23:23.867  3236  4657 D GhDiag  : relay dns -> 93B ok
10-25 10:23:23.871  3236  4659 D GhDiag  : relay dns -> 44B ok
10-25 10:23:25.266  3236  4676 D GhDiag  : relay dns -> 164B ok
10-25 10:23:25.267  3236  4678 D GhDiag  : relay dns -> 260B ok
10-25 10:23:25.573  3236  4686 D GhDiag  : relay tcp 172.217.x.x:443 -> socks5 ok
10-25 10:23:25.817  3236  4687 D GhDiag  : relay tcp 172.217.x.x:443 -> socks5 ok
10-25 10:23:25.904  3236  4692 D GhDiag  : relay tcp 1.1.x.x:443 -> socks5 ok

### e2e-xray-err.log (Xray core)

### e2e-vpn.log (GhVpnTunnel)
