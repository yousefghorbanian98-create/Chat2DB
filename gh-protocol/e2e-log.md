## gh-protocol E2E log — 2026-10-24T15:19:00Z

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
> Task :app:preBuild UP-TO-DATE
> Task :app:checkKotlinGradlePluginConfigurationErrors SKIPPED
> Task :app:preDebugBuild UP-TO-DATE
> Task :app:mergeDebugNativeDebugMetadata NO-SOURCE
> Task :app:createDebugCompatibleScreenManifests
> Task :app:generateDebugBuildConfig
> Task :app:generateDebugResValues
> Task :app:generateDebugResources
> Task :app:javaPreCompileDebug
> Task :app:mapDebugSourceSetPaths
> Task :app:extractDeepLinksDebug
> Task :app:checkDebugAarMetadata
> Task :app:packageDebugResources
> Task :app:mergeDebugShaders
> Task :app:compileDebugShaders NO-SOURCE
> Task :app:generateDebugAssets UP-TO-DATE
> Task :app:parseDebugLocalResources
> Task :app:desugarDebugFileDependencies
> Task :app:processDebugMainManifest
> Task :app:processDebugManifest
> Task :app:mergeDebugResources
> Task :app:mergeDebugJniLibFolders
> Task :app:processDebugManifestForPackage
> Task :app:checkDebugDuplicateClasses
> Task :app:mergeDebugAssets
> Task :app:mergeDebugNativeLibs
> Task :app:processDebugResources
> Task :app:mergeExtDexDebug
> Task :app:compressDebugAssets
> Task :app:mergeLibDexDebug

> Task :app:stripDebugDebugSymbols
Unable to strip the following libraries, packaging them as they are: libandroidx.graphics.path.so.

> Task :app:writeDebugAppMetadata
> Task :app:writeDebugSigningConfigVersions
> Task :app:validateSigningDebug

> Task :app:compileDebugKotlin
e: The daemon has terminated unexpectedly on startup attempt #1 with error code: 0. The daemon process output:
    1. Kotlin compile daemon is ready
w: file:///home/runner/work/Chat2DB/Chat2DB/gh-protocol/app/src/main/java/com/ghprotocol/app/MainActivity.kt:64:13 'fun updateConfiguration(p0: Configuration!, p1: DisplayMetrics!): Unit' is deprecated. Deprecated in Java.

> Task :app:processDebugJavaRes
> Task :app:mergeDebugJavaResource
> Task :app:compileDebugJavaWithJavac
> Task :app:dexBuilderDebug
> Task :app:mergeDebugGlobalSynthetics
> Task :app:mergeProjectDexDebug
> Task :app:packageDebug
> Task :app:assembleDebug
> Task :app:createDebugApkListingFileRedirect
gradle/actions: Writing build results to /home/runner/work/_temp/.gradle-actions/build-results/__run_2-1792854528407.json

BUILD SUCCESSFUL in 2m 4s
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
== launch app ==
  bash arg: -p
  bash arg: com.ghprotocol.app
  bash arg: -c
  bash arg: android.intent.category.LAUNCHER
  bash arg: 1
args: [-p, com.ghprotocol.app, -c, android.intent.category.LAUNCHER, 1]
 arg: "-p"
 arg: "com.ghprotocol.app"
 arg: "-c"
 arg: "android.intent.category.LAUNCHER"
 arg: "1"
data="com.ghprotocol.app"
data="android.intent.category.LAUNCHER"
// NOT RESPONDING: com.android.phone (pid 1200)
ANR in com.android.phone
PID: 1200
Reason: executing service com.android.phone/com.android.internal.telephony.CellularNetworkService
ErrorId: c5fdeb88-326b-48de-8151-d9144c68a44c
Frozen: false
Load: 0.0 / 0.0 / 0.0
----- Output from /proc/pressure/memory -----
some avg10=0.09 avg60=0.32 avg300=0.11 total=470536
full avg10=0.00 avg60=0.08 avg300=0.02 total=157384
----- End output from /proc/pressure/memory -----
----- Output from /proc/pressure/cpu -----
some avg10=88.07 avg60=84.57 avg300=50.55 total=244633142
full avg10=0.00 avg60=0.00 avg300=0.00 total=0
----- End output from /proc/pressure/cpu -----
----- Output from /proc/pressure/io -----
some avg10=2.04 avg60=2.73 avg300=3.00 total=22123481
full avg10=0.00 avg60=0.03 avg300=0.39 total=4507712
----- End output from /proc/pressure/io -----

CPU usage from 17198ms to -135ms ago (2026-10-24 15:17:50.578 to 2026-10-24 15:18:07.911):
  43% 537/system_server: 16% user + 26% kernel / faults: 5067 minor 2 major
  28% 1305/com.android.launcher3: 17% user + 10% kernel / faults: 5837 minor 2 major
  11% 143/vold: 2.9% user + 8.9% kernel / faults: 3 minor
  8.6% 1200/com.android.phone: 3.3% user + 5.3% kernel / faults: 2078 minor 1 major
  7.3% 924/com.android.systemui: 3.8% user + 3.5% kernel / faults: 2331 minor 1 major
  5.8% 2024/android.process.acore: 1.7% user + 4.1% kernel / faults: 640 minor
  4.9% 391/surfaceflinger: 1.5% user + 3.4% kernel / faults: 55 minor 1 major
  3.9% 347/android.hardware.sensors-service.multihal: 0.9% user + 2.9% kernel
  2.8% 40/kworker/1:1H-kblockd: 0% user + 2.8% kernel
  2.6% 934/com.android.permissioncontroller: 0.8% user + 1.8% kernel / faults: 126 minor
99% TOTAL: 32% user + 61% kernel + 0.1% iowait + 3.5% irq + 1.8% softirq
CPU usage from 405872ms to 405872ms ago (1970-01-01 00:00:00.000 to 1970-01-01 00:00:00.000) with 0% awake:
0% TOTAL: 0% user + 0% kernel

procrank:
<empty>

ZRAM: 0K physical used for 31232K in swap (1900908K total swap)
 RAM: 2534552K total, 169932K free, 131528K buffers, 1477444K cached, 3636K shmem, 146988K slab
// procrank status was 0
anr traces:
// anr traces status was 1
meminfo:

*** SERVICE 'meminfo' DUMP TIMEOUT (10000ms) EXPIRED ***


*** SERVICE 'meminfo' DUMP TIMEOUT (10000ms) EXPIRED ***

// meminfo status was 0
** Monkey aborted due to error.
Events injected: 0
## Network stats: elapsed time=20503ms (0ms mobile, 0ms wifi, 20503ms not connected)
== app alive? ==
pid after launch: <none>
--------- beginning of crash
10-24 15:18:31.727  2224  2383 F libc    : Fatal signal 6 (SIGABRT), code -1 (SI_QUEUE) in tid 2383 (bt_stack_manage), pid 2224 (droid.bluetooth)
=== E2E FAILED: app process not alive after launch (crash log attached) ===

### e2e-crash.log (crash buffer, tail)
--------- beginning of crash
10-24 15:18:31.727  2224  2383 F libc    : Fatal signal 6 (SIGABRT), code -1 (SI_QUEUE) in tid 2383 (bt_stack_manage), pid 2224 (droid.bluetooth)



